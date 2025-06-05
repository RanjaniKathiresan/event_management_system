# Mini Event Management System API

## 📝 Overview
A backend API for a simplified Event Management System built with Django and Django REST Framework. The system allows users to create events, register attendees, and view attendee lists per event.

---

## 📌 Features & Requirements
- **User Registration & Authentication** (Token-based)
- **Event Management**
  - Create events (`POST /events/`)
  - List all upcoming events (`GET /events/`)
- **Attendee Management**
  - Register attendee for an event (`POST /events/{event_id}/register/`)
    - Prevents overbooking (max_capacity)
    - Prevents duplicate registrations (by email)
  - List all attendees for an event (`GET /events/{event_id}/attendees/`)
- **Input Validation & Error Handling**
- **Swagger/OpenAPI Documentation**
- **Unit Tests** (using Django's unittest framework)

---

## 🛠️ Tech Stack
- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite
- **Documentation:** drf-yasg (Swagger/OpenAPI)

---

## 🚀 Setup Instructions

1. **Clone the repository**

   git clone git@github.com:RanjaniKathiresan/mini_event_management_api.git
   cd event_management_system
   
2. **Create and activate a virtual environment**

   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On Unix/Mac:
   source env/bin/activate

3. **Install dependencies**

   pip install -r requirements.txt

4. **Apply migrations**

   python manage.py migrate

5. **Run the development server**

   python manage.py runserver

6. **Access Swagger UI**
   - Visit `http://127.0.0.1:8000/swagger/` for interactive API docs.

---

## 🗄️ Database Schema
- See `events/models.py` and Django migrations for schema details.

---

## 🧪 Running Tests

python manage.py test events

---

## 📬 Sample API Requests

### Register User

curl -X POST http://127.0.0.1:8000/register/ -H "Content-Type: application/json" -d '{"username": "user1", "email": "user1@example.com", "password": "pass1234"}'


### Login

curl -X POST http://127.0.0.1:8000/login/ -H "Content-Type: application/json" -d '{"username": "user1", "password": "pass1234"}'


### Create Event

curl -X POST http://127.0.0.1:8000/events/ -H "Authorization: Token <your_token>" -H "Content-Type: application/json" -d '{"event_name": "Conference", "location": "Chennai", "start_time": "2025-06-10T10:00:00", "end_time": "2025-06-10T12:00:00", "max_capacity": 100, "is_active": true}'


### List Events

curl -X GET http://127.0.0.1:8000/events/ -H "Authorization: Token <your_token>"


### Register Attendee

curl -X POST http://127.0.0.1:8000/events/1/register/ -H "Authorization: Token <your_token>" -H "Content-Type: application/json" -d '{"attentee_name": "John Doe", "email_id": "john@example.com"}'


### List Attendees (paginated)

curl -X GET http://127.0.0.1:8000/events/1/attendees/ -H "Authorization: Token <your_token>"


---

## ⚙️ Assumptions
- All event times are provided in IST and stored in UTC.
- Only authenticated users can create events or register attendees.
- Duplicate attendee registration is prevented by email per event.

---

## 📦 Deliverables
- Source code
- README (this file)
- Database schema (via Django migrations)
- Unit tests
- Swagger/OpenAPI documentation

---
