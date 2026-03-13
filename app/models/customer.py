from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    signup_date = Column(DateTime(timezone=True), server_default=func.now())
    country = Column(String, nullable=True)
    acquisition_channel = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
