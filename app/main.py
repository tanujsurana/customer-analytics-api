from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine, Base
from app.models import Customer
from app.api.routes import customers
from app.api.routes import customers, events, analytics

app = FastAPI(title="Customer Analytics API")


Base.metadata.create_all(bind=engine)


app.include_router(customers.router)



app.include_router(events.router)


app.include_router(analytics.router)



@app.get("/")
def root():
    return {"message": "Customer Analytics API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-check")
def db_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database_connection": result.scalar()}


@app.get("/tables")
def list_tables():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        return {"tables": [row[0] for row in result]}
