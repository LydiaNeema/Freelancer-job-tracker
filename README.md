# Freelancer-job-tracker

# Freelancer Job Tracker (CLI + SQLAlchemy + Alembic)

## Setup
1) Create venv and install deps:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   # OR if required by rubric:
   pipenv --python 3.11
   pipenv install sqlalchemy alembic tabulate rich

2) Configure DB:
   - alembic.ini: sqlalchemy.url = sqlite:///./freelancer.db
   - alembic/env.py: import Base from app.database and set target_metadata = Base.metadata

3) Migrations:
   alembic revision --autogenerate -m "init"
   alembic upgrade head

4) Seed:
   python -m app.seed

5) Run CLI:
   python -m app.cli

## Features
- Customers, Invoices, Payments (SQLAlchemy ORM)
- CRUD for all entities
- Reports:
  - Customer Balances
  - Invoice Status Report (Paid/Partially/Unpaid)
  - Customer Statement
  - Revenue Summary
  - (Optional) Invoice Status Counts

## Tech
- SQLAlchemy, Alembic, Tabulate, Rich

## Notes
- Uses lists, tuples, dicts in CLI helpers.
- Validates user input in update/delete flows.
