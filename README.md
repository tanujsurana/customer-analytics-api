# Customer Analytics API Platform

A backend analytics system built using FastAPI, PostgreSQL, and SQLAlchemy that tracks customer activity events and provides analytics insights such as engagement metrics, churn risk detection, and retention summaries.

This project simulates how a real product analytics backend works by storing user events and computing behavior-based metrics through API endpoints.

--------------------------------------------------

## Architecture

Client / API User
↓
FastAPI Backend
↓
Pydantic Validation
↓
SQLAlchemy ORM
↓
PostgreSQL Database (Docker)

--------------------------------------------------

## Tech Stack

Backend Framework
- FastAPI

Database
- PostgreSQL (Docker)

ORM
- SQLAlchemy

Data Validation
- Pydantic

Fake Data Generation
- Faker

Server
- Uvicorn

Language
- Python 3

--------------------------------------------------

## Features

Customer Management
- Create customers
- Retrieve customers

Event Tracking
- Log customer activity events
- Retrieve all events

Analytics Endpoints
- Engagement summary
- Customer activity summary
- Date-range engagement analytics
- Churn risk detection
- Retention summary

Data Simulation
- Seed script generates realistic fake customer and event data.

--------------------------------------------------

## Project Structure
```
customer-analytics-api

app
 ├── api
 │    └── routes
 │         ├── customers.py
 │         ├── events.py
 │         └── analytics.py
 │
 ├── core
 │    └── database.py
 │
 ├── models
 │    ├── customer.py
 │    └── event.py
 │
 ├── schemas
 │    ├── customer.py
 │    ├── event.py
 │    └── analytics.py
 │
 └── main.py

scripts
 └── seed_data.py

docker-compose.yml
requirements.txt
README.md
```
--------------------------------------------------

## Setup Instructions

1. Clone repository

git clone <repo-url>
cd customer-analytics-api


2. Create virtual environment

python -m venv venv
source venv/bin/activate


3. Install dependencies

pip install -r requirements.txt


4. Start PostgreSQL using Docker

docker-compose up -d


5. Run the FastAPI server

uvicorn app.main:app --reload


API documentation available at:

http://127.0.0.1:8000/docs

--------------------------------------------------

## Seed Database with Sample Data

Generate realistic customers and events:

python -m scripts.seed_data

This will populate the database with fake customer activity data for testing analytics endpoints.

--------------------------------------------------

## API Endpoints

Customer APIs

POST /customers — create customer
GET /customers — list customers


Event APIs

POST /events — create event
GET /events — list events


Analytics APIs

GET /analytics/engagement-summary
GET /analytics/customer-activity
GET /analytics/events-by-date
GET /analytics/churn-risk
GET /analytics/retention-summary

--------------------------------------------------

## Example Analytics Output

{
  "total_events": 274,
  "active_customers": 52,
  "event_breakdown": {
    "login": 57,
    "purchase": 52,
    "feature_use": 51,
    "session_start": 53,
    "search": 61
  }
}

--------------------------------------------------

## Future Improvements

- Cohort retention curves
- Advanced churn prediction
- Event funnel analytics
- Dashboard visualization
- Scheduled analytics jobs
- Authentication layer

--------------------------------------------------

## Purpose of the Project

This project demonstrates how a backend analytics system can:

- track user behavior
- store event data
- compute engagement metrics
- detect churn indicators
- calculate retention statistics

It simulates the backend foundation used in real product analytics platforms.
