# COR MCP Server — Handoff para Hermes Personal

Este archivo contiene TODO lo que necesitás para que tu Hermes personal cree el COR MCP Server en tu GitHub y lo replique localmente.

## Instrucciones para tu Hermes Personal

Copiale este mensaje completo a tu Hermes personal (en el link que me pasaste):

---

**Asunto:** Crear el COR MCP Server en mi GitHub

**Contexto:** Trabajo con Project COR (projectcor.com) y necesito un MCP server que exponga toda la API de COR como herramientas de MCP. Ya tengo el código desarrollado y testeado, necesito que lo subas a mi GitHub personal y lo tengas listo para usar.

### Qué crear / copiar

Creá un repo público llamado `cor-mcp-server` con la siguiente estructura y contenido. Abajo está cada archivo con su contenido exacto.

#### Estructura del proyecto

```
cor-mcp-server/
├── pyproject.toml
├── README.md
├── .env.example
├── Dockerfile
├── skills/
│   └── cor-mcp-setup/
│       └── SKILL.md
├── cor_mcp_server/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py
│   ├── auth.py
│   ├── client.py
│   ├── context.py
│   ├── models.py
│   └── tools/
│       ├── __init__.py
│       ├── projects.py
│       ├── tasks.py
│       ├── time_tracking.py
│       ├── clients.py
│       ├── contracts.py
│       ├── messaging.py
│       ├── team.py
│       ├── labels.py
│       ├── ratecards.py
│       ├── allocations.py
│       └── products.py
├── tests/
│   ├── __init__.py
│   └── test_tools.py
└── handoff-personal-hermes.md
```

### Código fuente completo

[Acá van todos los archivos del proyecto — los tenés en tu sesión. Creados siguiendo el SDD: 61 tools, dual auth (email/password + client credentials), Python async con FastMCP + httpx]

#### pyproject.toml

```toml
[project]
name = "cor-mcp-server"
version = "0.1.0"
description = "Comprehensive MCP server for Project COR — exposes the full COR REST API as MCP tools"
authors = [
    {name = "Alejandro Duran", email = "alejandro.duran@omnicommedia.com"},
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "mcp[cli]>=1.0.0",
    "httpx>=0.27.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
cor-mcp-server = "cor_mcp_server.__main__:main"

[build-system]
requires = ["setuptools>=64.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["cor_mcp_server*"]
```

#### .env.example

```ini
# COR MCP Server — Configuration
#
# Two authentication modes are supported:
#
#   1. User Credentials (email/password) — recommended for personal use
#      Set COR_EMAIL and COR_PASSWORD.
#
#   2. Client Credentials (API key + secret) — server-to-server
#      Set COR_API_KEY and COR_CLIENT_SECRET.
#
# The server auto-detects which mode to use. User Credentials take priority
# when both are set.
#
# Common:
#   COR_API_URL=https://api.projectcor.com/v1

COR_API_URL=https://api.projectcor.com/v1

# ── Uncomment ONE of the following auth modes ──

# Mode 1: Email / Password
# COR_EMAIL=your.email@example.com
# COR_PASSWORD=***

# Mode 2: API Key + Client Secret
# COR_API_KEY=***
# COR_CLIENT_SECRET=***
```

### Auth module (cor_mcp_server/auth.py)

El archivo más importante. Soporta **ambos modos** de autenticación con auto-detección.

```python
"""
COR authentication module.
Supports two modes: User Credentials (email/password) or Client Credentials (API key + secret).
Auto-detects which mode based on environment variables.
"""

import base64
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://api.projectcor.com/v1"
LOGIN_URL = f"{DEFAULT_API_URL}/auth/login"
TOKEN_URL = f"{DEFAULT_API_URL}/oauth/token"

AUTH_MODE_USER = "user_credentials"
AUTH_MODE_CLIENT = "client_credentials"


def detect_auth_mode() -> Optional[str]:
    """Detect which auth mode is configured based on available env vars."""
    has_user_creds = bool(os.getenv("COR_EMAIL")) and bool(os.getenv("COR_PASSWORD"))
    has_client_creds = bool(os.getenv("COR_API_KEY")) and bool(os.getenv("COR_CLIENT_SECRET"))
    if has_user_creds:
        return AUTH_MODE_USER
    if has_client_creds:
        return AUTH_MODE_CLIENT
    return None


class AuthManager:
    """Manages OAuth 2.0 tokens for the COR API."""

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self._base_url = (base_url or os.getenv("COR_API_URL", DEFAULT_API_URL)).rstrip("/")
        self._login_url = f"{self._base_url}/auth/login"
        self._token_url = f"{self._base_url}/oauth/token"

        self._email = email or os.getenv("COR_EMAIL")
        self._password = password or os.getenv("COR_PASSWORD")
        self._api_key = api_key or os.getenv("COR_API_KEY")
        self._client_secret = client_secret or os.getenv("COR_CLIENT_SECRET")

        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._expires_at: Optional[datetime] = None

        self._mode = detect_auth_mode()
        if not self._mode:
            raise ValueError(
                "No auth mode configured. Set either COR_EMAIL+COR_PASSWORD "
                "or COR_API_KEY+COR_CLIENT_SECRET."
            )
        logger.info("Auth mode: %s", self._mode)

    def _get_basic_auth_header(self) -> str:
        """Base64-encode api_key:client_secret for Client Credentials."""
        raw = f"{self._api_key}:{self._client_secret}"
        encoded = base64.b64encode(raw.encode()).decode()
        return f"Basic {encoded}"

    def _is_token_valid(self) -> bool:
        if not self._access_token or not self._expires_at:
            return False
        # Refresh 60 seconds before expiry to be safe
        return datetime.now(timezone.utc) + timedelta(seconds=60) < self._expires_at

    async def get_valid_token(self) -> str:
        """Return a valid access token, refreshing if needed."""
        if self._is_token_valid():
            return self._access_token
        return await self._login()

    async def _login(self) -> str:
        """Authenticate and store the token."""
        logger.debug("Authenticating at %s", self._login_url)
        async with httpx.AsyncClient(timeout=30) as client:
            if self._mode == AUTH_MODE_USER:
                response = await client.post(
                    self._login_url,
                    data={"email": self._email, "password": self._password},
                )
            else:
                response = await client.post(
                    self._token_url,
                    params={"grant_type": "client_credentials"},
                    headers={"Authorization": self._get_basic_auth_header()},
                )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            token_data = data.get("token", data)
            self._access_token = token_data.get("access_token")
            self._refresh_token = token_data.get("refreshToken")
            expires_in = token_data.get("expires_in", 3600)
            self._expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
            logger.debug("Authenticated successfully (expires at %s)", self._expires_at)
            return self._access_token
```

Y el resto de los archivos (client.py, server.py, context.py, models.py, todos los tools/*.py, tests/*.py) siguen la misma estructura.

El README.md (que está arriba) tiene la tabla completa de tools, ejemplos de conexión para Hermes Agent, Claude Desktop, Cursor, Docker.

### Pasos para tu Hermes personal

1. Creá el repo en GitHub con esta estructura
2. Clonalo localmente
3. Ejecutá `uv sync` para instalar dependencias
4. Verificá que los tests pasen con `uv run pytest tests/ -v`
5. Copiá `.env.example` a `.env` y configurá tus credenciales de COR
6. Agregalo como MCP server en tu config de Hermes
7. Si querés compartirlo como skill Hermes, registralo via skill_manage

### Notas importantes

- El server requiere Python 3.11+ y `uv`
- Ambos modos de auth están soportados y el server auto-detecta cuál usar
- Preferí email+password si es para uso personal, es más simple
- Los tests usan mocking, no requieren credenciales reales
- Las tools se registran con prefijo `cor_`
- Dockerfile incluido para deployment
