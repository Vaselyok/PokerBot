from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from .common import BaseShortResponse, to_moscow
from .table import TableShortResponse
from .tgchat import TgchatShortResponse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class GameResponse(BaseModel):
    id: int
    name: str
    start_time: datetime | None
    status: str
    organizer: BaseShortResponse
    players: list[BaseShortResponse] | None
    tables: list[TableShortResponse] | None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("start_time")
    def serialize_start_time(self, dt):
        return to_moscow(dt)


class GamePatchRequest(BaseModel):
    name: str | None = Field(None, min_length=1)
    is_archived: bool | None = None
    start_time: datetime | None = None

    model_config = {"extra": "forbid"}

    @field_validator("start_time")
    def normalize_datetime(cls, dt):
        if dt is None:
            return None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))

        return dt.astimezone(timezone.utc)


class GameAddRequest(BaseModel):
    name: str = Field(min_length=1)
    start_time: datetime
    chat_id: int | None = None

    model_config = {"extra": "forbid"}

    @field_validator("start_time")
    def normalize_datetime(cls, dt):
        if dt is None:
            return None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))

        return dt.astimezone(timezone.utc)


class GPPlayerResponse(BaseModel):
    game_id: int
    player: BaseShortResponse
    status: str

    model_config = ConfigDict(from_attributes=True)


class GamePlayerList(BaseModel):
    items: list[GPPlayerResponse]
    total: int
    limit: int
    offset: int


class TablePlayerDistribute(BaseModel):
    id: int
    name: str
    telegram_id: int


class TableDistribute(BaseModel):
    id: int
    number: int
    players: list[TablePlayerDistribute]


class DistributeTablesResponse(BaseModel):
    game_id: int
    chat_id: int | None
    thread_id: int | None
    tables: list[TableDistribute]
