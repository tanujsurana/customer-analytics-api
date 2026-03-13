from pydantic import BaseModel
from datetime import datetime


class EngagementSummaryResponse(BaseModel):
    total_events: int
    active_customers: int
    event_breakdown: dict[str, int]


class CustomerActivityResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    total_events: int
    last_activity: datetime | None


class DateRangeEngagementResponse(BaseModel):
    start_date: datetime
    end_date: datetime
    total_events: int
    active_customers: int
    event_breakdown: dict[str, int]


class ChurnRiskCustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    last_activity: datetime | None


class ChurnRiskResponse(BaseModel):
    cutoff_date: datetime
    churn_risk_count: int
    customers: list[ChurnRiskCustomerResponse]

class RetentionSummaryResponse(BaseModel):
    cohort_date: datetime
    total_customers: int
    retained_customers: int
    retention_rate: float
