# 🚌 Lavasa Bus Booking System

A full-stack Django web application for managing the Lavasa ↔ Pune university bus service.

---

## Features

- **Roles**: Student, Faculty, Admin — each with tailored UI
- **Weekend Bus Service**: Sundays only, Lavasa→Pune 10AM / Pune→Lavasa 6PM (configurable)
- **Vacation Bus Service**: Custom dates, one-way only, no reason/proof required
- **Merged Slots**: Admin enables "Create Return Slot" → users choose one-way or both-ways in one booking
- **Seat Limit**: 45 seats per slot (configurable per slot)
- **One-way booking**: Requires reason + proof upload (for students, weekend service)
- **Faculty booking**: Relaxed form — reason/proof optional
- **Student fields**: Year of Study (1st–5th), Department
- **Admin dashboard**: Stats, approve/cancel/revert bookings, add/edit/delete slots, manage users
- **Real-time updates**: All admin changes instantly reflect for users
- **Permanent deletion**: Deleted slots are fully removed (not soft-deleted)

---

## Quick Start

### 1. Install Python & Django

```bash
pip install -r requirements.txt
```

### 2. Run Setup (creates DB, admin user, sample slots)

```bash
cd busproject
python setup.py
```

This creates:
- SQLite database with all tables
- Admin account: `username=admin` / `password=admin123`
- One sample Weekend slot (next Sunday, Lavasa→Pune + return)
- One sample Vacation slot (2 weeks from today)

### 3. Start the Server

```bash
python manage.py runserver
```

### 4. Open in Browser

Visit: **http://127.0.0.1:8000/**

---

## Default Accounts

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |

Create Student/Faculty accounts via the Sign Up page.

---

## Project Structure

```
busproject/
├── manage.py
├── setup.py              ← Run once to initialize
├── requirements.txt
├── busproject/
│   ├── settings.py
│   └── urls.py
└── busapp/
    ├── models.py         ← User, BusSlot, Booking
    ├── views.py          ← All page logic
    ├── forms.py          ← All form classes
    ├── urls.py           ← URL routing
    ├── admin.py
    ├── migrations/
    ├── templates/busapp/
    │   ├── base.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── dashboard.html        ← Student/Faculty view
    │   ├── book_student.html
    │   ├── book_faculty.html
    │   ├── admin_dashboard.html
    │   ├── admin_slot_form.html  ← Add & Edit slots
    │   ├── admin_slot_bookings.html
    │   └── admin_users.html
    └── static/busapp/
        ├── css/style.css
        └── js/main.js
```

---

## How It Works

### Weekend Service (Merged Slots)
When admin creates a Weekend slot and enables **"Enable Return Journey"**:
- The return leg details (time, route, seats) are stored in the same `BusSlot` record
- Users see the outward + return info on the dashboard
- On booking, they choose **One Way** or **Both Ways** — one booking record handles both
- One-way on Weekend service requires: reason text + proof file upload

### Vacation Service
- No return journey option
- No route toggle (admin sets fixed route)
- No reason/proof required
- One-way only

### Admin Controls
- **Add Slot**: Set service type, date, route, departure time, seat limit, description, optional return
- **Edit Slot**: Same form pre-filled; all fields editable including return toggle
- **Delete Slot**: Permanently deleted (with all its bookings)
- **Approve/Cancel Booking**: With optional admin note; user sees status update instantly
- **Revert Booking**: Change approved/cancelled back to pending

---

## Tech Stack

- **Backend**: Django 4.2 (Python)
- **Database**: SQLite (easy swap to PostgreSQL for production)
- **Frontend**: Bootstrap 5.3 + custom CSS (pastel theme) + Vanilla JS
- **File uploads**: Django FileField → `/media/proofs/`
- **Auth**: Django's built-in auth with custom User model (role field)

---

## Notes for Production

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure proper database (PostgreSQL recommended)
4. Set up static file serving (WhiteNoise or Nginx)
5. Use environment variables for sensitive settings
