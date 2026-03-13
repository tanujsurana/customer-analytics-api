from pydantic import BaseModel
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    email: str
    country: str | None = None
    acquisition_channel: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    signup_date: datetime
    country: str | None
    acquisition_channel: str | None
    status: str

    class Config:
        from_attributes = True
