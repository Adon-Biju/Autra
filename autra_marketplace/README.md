# Autra - AI Workforce Marketplace

The first AI workforce platform where businesses hire AI employees and developers get paid for building them.

## Features
- 🤖 Browse and hire AI agents
- 💰 Multiple pricing models (one-time, subscription, usage-based)
- 🔒 Sandbox testing environment
- ⭐ Trust-based rankings
- 💳 Secure payment processing with Stripe

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## Tech Stack
- Django 5.0
- PostgreSQL
- Redis & Celery
- Stripe Connect
- Docker
