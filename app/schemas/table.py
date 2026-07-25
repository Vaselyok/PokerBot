from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from .common import BaseShortResponse, to_moscow
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Literal



class TableCountResponse(BaseModel):
    id: int
    number: int
    total_participants: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TableShortResponse(BaseModel):
    id: int
    number: int

    model_config = ConfigDict(from_attributes=True)


class TableListResponse(BaseModel):
    items: list[TableCountResponse]
    total: int
    limit: int
    offset: int


class TableResponse(BaseModel):
    id: int
    number: int
    started_at: datetime | None
    finished_at: datetime | None
    players: list[BaseShortResponse] | None = None
    game: BaseShortResponse

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("started_at", "finished_at")
    def serialize_datetime(self, dt):
        return to_moscow(dt)
    
    
class TablesAddRequest(BaseModel):
    total_tables: int = Field(gt=0)
    model_config = {"extra": "forbid"}


class TablePatchRequest(BaseModel):
    started_at: datetime | None = None
    finished_at: datetime | None = None

    model_config = {"extra": "forbid"}

    @field_validator("started_at", "finished_at")
    def normalize_datetime(cls, dt):
        if dt is None:
            return None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))

        return dt.astimezone(timezone.utc)