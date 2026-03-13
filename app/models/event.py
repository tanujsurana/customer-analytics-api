from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Event(Base):
    __tablename__ = "customer_events"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    event_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    event_value = Column(Integer, nullable=True)
