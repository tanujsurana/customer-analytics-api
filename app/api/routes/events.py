from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.customer import Customer
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == event.customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_event = Event(
        customer_id=event.customer_id,
        event_type=event.event_type,
        event_value=event.event_value,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get("/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events
