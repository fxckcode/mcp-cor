"""
Pydantic models for Project COR API data structures.

Provides type-safe, validated data models for common COR entities.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CORBaseModel(BaseModel):
    """Base model with common configuration."""

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        extra = "allow"


class Project(CORBaseModel):
    """Project COR model."""
    id: int | str | None = None
    name: str | None = None
    description: str | None = None
    status: str | None = None
    client_id: int | str | None = Field(None, alias="clientId")
    project_manager_id: int | str | None = Field(None, alias="projectManagerId")
    start_date: str | None = Field(None, alias="startDate")
    end_date: str | None = Field(None, alias="endDate")
    budget: float | None = None
    health: str | None = None
    created_at: str | None = Field(None, alias="createdAt")
    updated_at: str | None = Field(None, alias="updatedAt")


class Task(CORBaseModel):
    """Task COR model."""
    id: int | str | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
    project_id: int | str | None = Field(None, alias="projectId")
    assignee_id: int | str | None = Field(None, alias="assigneeId")
    deadline: str | None = None
    priority: str | None = None
    created_at: str | None = Field(None, alias="createdAt")
    updated_at: str | None = Field(None, alias="updatedAt")


class Client(CORBaseModel):
    """Client COR model."""
    id: int | str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    notes: str | None = None
    created_at: str | None = Field(None, alias="createdAt")
    updated_at: str | None = Field(None, alias="updatedAt")


class Contract(CORBaseModel):
    """Contract COR model."""
    id: int | str | None = None
    name: str | None = None
    client_id: int | str | None = Field(None, alias="clientId")
    status: str | None = None
    start_date: str | None = Field(None, alias="startDate")
    end_date: str | None = Field(None, alias="endDate")
    value: float | None = None
    created_at: str | None = Field(None, alias="createdAt")


class TimeEntry(CORBaseModel):
    """Time entry COR model."""
    id: int | str | None = None
    task_id: int | str | None = Field(None, alias="taskId")
    user_id: int | str | None = Field(None, alias="userId")
    date: str | None = None
    hours: float | None = None
    notes: str | None = None
    status: str | None = None
    created_at: str | None = Field(None, alias="createdAt")


class User(CORBaseModel):
    """User COR model."""
    id: int | str | None = None
    name: str | None = None
    email: str | None = None
    role: str | None = None
    avatar_url: str | None = Field(None, alias="avatarUrl")
    created_at: str | None = Field(None, alias="createdAt")


class Team(CORBaseModel):
    """Team COR model."""
    id: int | str | None = None
    name: str | None = None
    description: str | None = None
    created_at: str | None = Field(None, alias="createdAt")


class Label(CORBaseModel):
    """Label COR model."""
    id: int | str | None = None
    name: str | None = None
    color: str | None = None
    entity: str | None = None


class Ratecard(CORBaseModel):
    """Ratecard COR model."""
    id: int | str | None = None
    name: str | None = None
    description: str | None = None
    created_at: str | None = Field(None, alias="createdAt")


class Allocation(CORBaseModel):
    """Resource allocation COR model."""
    id: int | str | None = None
    project_id: int | str | None = Field(None, alias="projectId")
    user_id: int | str | None = Field(None, alias="userId")
    allocation_percentage: float | None = Field(None, alias="allocationPercentage")
    start_date: str | None = Field(None, alias="startDate")
    end_date: str | None = Field(None, alias="endDate")


class Product(CORBaseModel):
    """Product COR model."""
    id: int | str | None = None
    name: str | None = None
    description: str | None = None
    rate: float | None = None
    created_at: str | None = Field(None, alias="createdAt")


class ContractPosition(CORBaseModel):
    """Contract position COR model."""
    id: int | str | None = None
    contract_id: int | str | None = Field(None, alias="contractId")
    title: str | None = None
    rate: float | None = None
    hours: float | None = None
    created_at: str | None = Field(None, alias="createdAt")


class Message(CORBaseModel):
    """Message COR model."""
    id: int | str | None = None
    content: str | None = None
    user_id: int | str | None = Field(None, alias="userId")
    created_at: str | None = Field(None, alias="createdAt")


class WorkingTime(CORBaseModel):
    """Working time COR model."""
    id: int | str | None = None
    user_id: int | str | None = Field(None, alias="userId")
    day: str | None = None
    hours: float | None = None
    start_time: str | None = Field(None, alias="startTime")
    end_time: str | None = Field(None, alias="endTime")
