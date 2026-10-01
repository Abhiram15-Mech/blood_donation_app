# LifeDrop — Blood Donation & Blood Bank Management System

A beginner-friendly web application built with Python, Bottle, SQLite3, HTML, CSS and vanilla JavaScript.

## Features

- User registration/login
- Password hashing
- Donor registration and profile
- Donor search by blood group/city/state
- Blood bank search
- Blood inventory
- Blood request workflow
- Donation history
- Admin dashboard
- SQLite database
- JSON API endpoints
- Responsive frontend

## Ubuntu installation

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv sqlite3

cd blood_donation_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start:

```bash
python3 app.py
```

Open:

http://localhost:8080

The database is created automatically on first start.

## Demo accounts

Admin:

- Email: `admin@lifedrop.local`
- Password: `admin123`

Sample normal users:

- `arun@example.local` / `password123`
- `priya@example.local` / `password123`

## SQLite

To inspect the database:

```bash
sqlite3 blood_donation.db
.tables
.schema users
SELECT * FROM users;
.quit
```

## Main routes

- `/`
- `/register`
- `/login`
- `/dashboard`
- `/donate`
- `/donor-profile`
- `/find-blood`
- `/find-donors`
- `/blood-banks`
- `/blood-availability`
- `/request-blood`
- `/donation-history`
- `/admin`

## JSON API

- `/api/blood-availability`
- `/api/donors`
- `/api/blood-banks`

Example:

```bash
curl http://localhost:8080/api/blood-availability
```

## Project structure

```text
blood_donation_app/
├── app.py
├── auth.py
├── database.py
├── blood_donation.db       # generated on first run
├── requirements.txt
├── README.md
├── views/
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Learning order

1. Read `database.py` to understand tables.
2. Read `app.py` and learn Bottle routes.
3. Open `views/index.tpl` to understand HTML.
4. Read `static/css/style.css`.
5. Read `static/js/app.js`.
6. Try registration and login.
7. Inspect changes with SQLite.
8. Test JSON APIs with curl.

## Important

This is an educational/demo application. Real blood availability, donor eligibility, medical decisions, emergency coordination, and blood-bank operations must be handled by qualified professionals and authorized organizations.
# blood_donation_app
# blood_donation_app
