from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.event import Event
from app.models.customer import Customer
from app.schemas.analytics import (
    EngagementSummaryResponse,
    CustomerActivityResponse,
    DateRangeEngagementResponse,
    ChurnRiskCustomerResponse,
    ChurnRiskResponse,
    RetentionSummaryResponse,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/engagement-summary", response_model=EngagementSummaryResponse)
def get_engagement_summary(db: Session = Depends(get_db)):
    total_events = db.query(func.count(Event.id)).scalar() or 0

    active_customers = db.query(func.count(func.distinct(Event.customer_id))).scalar() or 0

    event_rows = (
        db.query(Event.event_type, func.count(Event.id))
        .group_by(Event.event_type)
        .all()
    )

    event_breakdown = {event_type: count for event_type, count in event_rows}

    return EngagementSummaryResponse(
        total_events=total_events,
        active_customers=active_customers,
        event_breakdown=event_breakdown,
    )


@router.get("/customer-activity", response_model=list[CustomerActivityResponse])
def get_customer_activity(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Customer.id.label("customer_id"),
            Customer.name,
            Customer.email,
            func.count(Event.id).label("total_events"),
            func.max(Event.event_time).label("last_activity"),
        )
        .join(Event, Event.customer_id == Customer.id)
        .group_by(Customer.id, Customer.name, Customer.email)
        .order_by(func.count(Event.id).desc())
        .all()
    )

    return [
        CustomerActivityResponse(
            customer_id=row.customer_id,
            name=row.name,
            email=row.email,
            total_events=row.total_events,
            last_activity=row.last_activity,
        )
        for row in rows
    ]

@router.get("/events-by-date", response_model=DateRangeEngagementResponse)
def get_events_by_date(
    start_date: datetime = Query(..., description="Start date in ISO format"),
    end_date: datetime = Query(..., description="End date in ISO format"),
    db: Session = Depends(get_db),
):
    filtered_events = db.query(Event).filter(
        Event.event_time >= start_date,
        Event.event_time <= end_date
    )

    total_events = filtered_events.count()

    active_customers = (
        db.query(func.count(func.distinct(Event.customer_id)))
        .filter(Event.event_time >= start_date, Event.event_time <= end_date)
        .scalar()
        or 0
    )

    event_rows = (
        db.query(Event.event_type, func.count(Event.id))
        .filter(Event.event_time >= start_date, Event.event_time <= end_date)
        .group_by(Event.event_type)
        .all()
    )

    event_breakdown = {event_type: count for event_type, count in event_rows}

    return DateRangeEngagementResponse(
        start_date=start_date,
        end_date=end_date,
        total_events=total_events,
        active_customers=active_customers,
        event_breakdown=event_breakdown,
    )

@router.get("/churn-risk", response_model=ChurnRiskResponse)
def get_churn_risk(
    cutoff_date: datetime = Query(..., description="Customers inactive before this datetime are considered at churn risk"),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(
            Customer.id.label("customer_id"),
            Customer.name,
            Customer.email,
            func.max(Event.event_time).label("last_activity"),
        )
        .join(Event, Event.customer_id == Customer.id)
        .group_by(Customer.id, Customer.name, Customer.email)
        .having(func.max(Event.event_time) < cutoff_date)
        .order_by(func.max(Event.event_time).asc())
        .all()
    )

    customers = [
        ChurnRiskCustomerResponse(
            customer_id=row.customer_id,
            name=row.name,
            email=row.email,
            last_activity=row.last_activity,
        )
        for row in rows
    ]

    return ChurnRiskResponse(
        cutoff_date=cutoff_date,
        churn_risk_count=len(customers),
        customers=customers,
    )


@router.get("/retention-summary", response_model=RetentionSummaryResponse)
def get_retention_summary(
    cohort_date: datetime = Query(..., description="Customers who signed up on or before this date are included in the cohort"),
    db: Session = Depends(get_db),
):
    cohort_customers = db.query(Customer).filter(Customer.signup_date <= cohort_date).all()
    total_customers = len(cohort_customers)

    if total_customers == 0:
        return RetentionSummaryResponse(
            cohort_date=cohort_date,
            total_customers=0,
            retained_customers=0,
            retention_rate=0.0,
        )

    cohort_customer_ids = [customer.id for customer in cohort_customers]

    retained_customers = (
        db.query(func.count(func.distinct(Event.customer_id)))
        .filter(
            Event.customer_id.in_(cohort_customer_ids),
            Event.event_time > cohort_date,
        )
        .scalar()
        or 0
    )

    retention_rate = (retained_customers / total_customers) * 100

    return RetentionSummaryResponse(
        cohort_date=cohort_date,
        total_customers=total_customers,
        retained_customers=retained_customers,
        retention_rate=round(retention_rate, 2),
    )


