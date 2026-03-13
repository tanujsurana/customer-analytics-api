from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    customer_id: int
    event_type: str
    event_value: int | None = None


class EventResponse(BaseModel):
    id: int
    customer_id: int
    event_type: str
    event_time: datetime
    event_value: int | None

    class Config:
        from_attributes = True
