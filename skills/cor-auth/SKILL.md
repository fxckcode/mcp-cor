---
name: cor-auth
description: "Authentication cheat sheet for the COR MCP Server — covers both auth modes (email/password and client credentials) step by step, token refresh mechanism, and common auth errors."
version: 1.0.0
plugin: false
---

# COR Auth — Cheat Sheet

## Overview

The COR MCP Server supports **two authentication modes** with auto-detection. The server checks env vars at startup and picks the right flow automatically.

| Mode | Env Vars | Use Case |
|------|----------|----------|
| **User Credentials** | `COR_EMAIL` + `COR_PASSWORD` | Personal use, testing, single-user agents |
| **Client Credentials** | `COR_API_KEY` + `COR_CLIENT_SECRET` | Server-to-server, automated workflows |

**Priority:** User Credentials (email/password) takes priority when both are set. To use Client Credentials, leave email/password unset.

---

## Mode A: User Credentials (Email + Password)

### Step-by-Step

1. **Set environment variables:**
   ```ini
   COR_EMAIL=your.email@company.com
   COR_PASSWORD=your_secret_password
   COR_API_URL=https://api.projectcor.com/v1
   ```

2. **Server detects auth mode** → `"Auth mode: User Credentials (email/password)"`

3. **On first API call**, the server sends:
   ```
   POST https://api.projectcor.com/v1/auth/login
   Content-Type: application/x-www-form-urlencoded
   Accept: application/json

   email=your.email@company.com&password=your_secret_password
   ```

4. **COR API responds** with one of these shapes:
   ```json
   // Shape 1 — direct token
   {"access_token": "eyJ...", "expires_in": 3600}

   // Shape 2 — nested token object
   {"token": {
       "access_token": "eyJ...",
       "type": "bearer",
       "refreshToken": "rt_...",
       "expirationTime": "1712345678000"
   }}

   // Shape 3 — data wrapper
   {"data": {"token": "eyJ..."}}
   ```

5. **Token is cached** in the `TokenStore` (thread-safe, in-memory).

6. **Subsequent API calls** reuse the cached token until it's within 60 seconds of expiry, then auto-refresh.

### Email/Password Auth Flow Diagram

```
┌─────────┐         ┌──────────────┐         ┌──────────────┐
│ Hermes  │  tool   │  COR MCP     │  POST    │  COR API     │
│ Agent   │────────►│  Server      │─────────►│  /auth/login │
│         │         │              │◄─────────┤              │
│         │         │  TokenStore  │  JWT     │              │
│         │         │  cache       │          └──────────────┘
└─────────┘         └──────────────┘
```

### Python Equivalent

What the code does internally in `auth.py`:

```python
async def _login(self) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            self._login_url,  # e.g. https://api.projectcor.com/v1/auth/login
            data={"email": self._email, "password": self._password},
            headers={"Accept": "application/json"},
        )
        data = response.json()
        # Normalises token response:
        # - Looks for "access_token" at root
        # - Falls back to data["token"]["access_token"]
        # - Falls back to data["token"] (string)
        # - Falls back to data["data"]["token"]
        return data
```

---

## Mode B: Client Credentials (API Key + Secret)

### Step-by-Step

1. **Set environment variables:**
   ```ini
   COR_API_KEY=your_api_key_here
   COR_CLIENT_SECRET=your_client_secret_here
   COR_API_URL=https://api.projectcor.com/v1
   ```

2. **Server detects auth mode** → `"Auth mode: Client Credentials (API key/secret)"`

3. **On first API call**, the server creates a Basic auth header:
   ```
   Authorization: Basic base64(api_key:client_secret)
   ```
   Then posts to the token endpoint:
   ```
   POST https://api.projectcor.com/v1/oauth/token?grant_type=client_credentials
   Authorization: Basic ZGZjYzA...==
   Accept: application/json
   ```

4. **COR API responds:**
   ```json
   {"access_token": "eyJ...", "expires_in": 3600}
   ```

5. **Token is cached** with 1-hour TTL. Auto-refreshed with a 60-second safety margin.

### Client Credentials Flow Diagram

```
┌─────────┐         ┌──────────────┐         ┌────────────────────┐
│ Hermes  │  tool   │  COR MCP     │  POST    │  COR API          │
│ Agent   │────────►│  Server      │─────────►│  /oauth/token     │
│         │         │              │◄─────────┤  ?grant_type=     │
│         │         │  TokenStore  │  JWT     │  client_credentials│
│         │         │  cache       │          └────────────────────┘
└─────────┘         └──────────────┘
```

### Python Equivalent

What the code does internally in `auth.py`:

```python
def _get_basic_auth_header(self) -> str:
    credentials = f"{self._api_key}:{self._client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"

async def _client_credentials_grant(self) -> dict[str, Any]:
    headers = {
        "Authorization": self._get_basic_auth_header(),
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            self._token_url,
            headers=headers,
        )
        if response.status_code != 200:
            raise AuthError(...)
        return response.json()
```

---

## Token Refresh Mechanism

The `TokenStore` class manages automatic token refresh:

```python
TOKEN_REFRESH_MARGIN = 60  # seconds

class TokenStore:
    def set_token(self, access_token: str, expires_in: int) -> None:
        # Stores token + calculates expiry as time.time() + expires_in

    def is_expired(self) -> bool:
        # Returns True if time.time() >= (expires_at - 60 seconds)
```

**Refresh flow:**
1. Before every API call, `AuthManager.get_access_token()` checks `is_expired()`
2. If not expired and token exists → return cached token immediately
3. If expired or missing → call `_fetch_token()` (login or client credentials grant)
4. Store new token with new expiry
5. Return fresh token

This means the server **never blocks** on a mid-request expiry — it refreshes proactively at the 60-second margin.

### Note on Refresh Tokens

**User Credentials mode** may return a `refreshToken` from COR's login endpoint, but the current implementation **re-authenticates** (calls login again) rather than using a dedicated refresh endpoint. This is simpler and works because the login response returns a new token pair each time.

**Client Credentials mode** does not use refresh tokens — it simply requests a new token via the same client credentials grant.

---

## Common Auth Errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `No COR credentials found` | Neither auth mode configured | Set `COR_EMAIL`+`COR_PASSWORD` or `COR_API_KEY`+`COR_CLIENT_SECRET` |
| `Token acquisition failed: HTTP 401` | Invalid API key or client secret | Double-check `COR_API_KEY` and `COR_CLIENT_SECRET` in `.env` |
| `Login failed: HTTP 401` | Wrong email/password | Verify `COR_EMAIL` and `COR_PASSWORD` |
| `Token acquisition failed: HTTP 403` | API key lacks permissions | Check with COR admin that the key has the right scopes |
| `No access_token in token response` | Unexpected API response shape | Check COR API version compatibility. Try updating the server |
| `AuthError: No access_token...` | Login succeeded but response format unknown | May need to update `_login()` response normalisation |
| `Auth not configured` (at startup) | Missing all auth env vars | Set credentials before starting the server |
| Token errors after long idle | Token expired and refresh failed | Ensure credentials are still valid. Restart server to force fresh login |
| `COR_EMAIL and COR_PASSWORD must be set` | Mode detected as user_credentials but vars are empty | Set both `COR_EMAIL` and `COR_PASSWORD` |
| `HTTP 400 Bad Request` during client credentials | Missing or malformed Basic auth header | Ensure `COR_API_KEY` contains no special characters. Check base64 encoding |

## Configuration Quick Reference

### `.env` File Template

```ini
# REQUIRED — API base URL
COR_API_URL=https://api.projectcor.com/v1

# ── Pick ONE auth mode (uncomment the pair) ──

# Mode A: Email + Password (personal use)
# COR_EMAIL=your.email@company.com
# COR_PASSWORD=your_password

# Mode B: API Key + Client Secret (server-to-server)
# COR_API_KEY=your_api_key
# COR_CLIENT_SECRET=your_client_secret
```

### Hermes Agent Config

```yaml
mcp_servers:
  cor:
    command: "uv"
    args: ["run", "--directory", "/path/to/cor-mcp-server", "python", "-m", "cor_mcp_server"]
    env:
      COR_EMAIL: "your.email@company.com"
      COR_PASSWORD: "your_password"
      COR_API_URL: "https://api.projectcor.com/v1"
    timeout: 180
    connect_timeout: 60
```

## Verification

After configuring auth, verify it works:

```bash
# Terminal check — starts server and checks auth detection
uv run cor-mcp-server --verbose
# Look for: "Auth mode: User Credentials (email/password)" or
#           "Auth mode: Client Credentials (API key/secret)"

# In Hermes, after /reload-mcp:
# Ask: "what's my COR profile"
# If it returns user data → auth is working
```

## Security Notes

- **Never commit `.env` files** with real credentials to git. `.env.example` is the template.
- The `COR_CLIENT_SECRET` and `COR_PASSWORD` are sensitive — treat them like any credential.
- Tokens are stored **in memory only** (Python process memory). They are never written to disk.
- The 60-second refresh margin means a token could be reused for up to 60 seconds after expiry in edge cases, but this is safe for the server's use pattern.
- If running in SSE/HTTP mode, ensure the server is behind a firewall or VPN — it does not implement authentication for the SSE endpoint itself (auth is only for the upstream COR API).
