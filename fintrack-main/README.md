# FinTrack – Personal Finance Management System

FinTrack is a production-quality Personal Finance Management System built with Python, Django 5, and MySQL. This repository contains the foundation and initial project architecture.

## Technology Stack
- **Backend:** Python, Django 5
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (using customized Google Stitch UI components)
- **Database:** MySQL
- **Environment Management:** python-dotenv (for production-ready environment configuration)

---

## Folder Structure
The project layout is structured as follows:

```text
fintrack/
├── .gitignore               # Standard Python & Django Git exclusions
├── README.md                # Project documentation and setup guide
├── requirements.txt         # Core dependencies
├── manage.py                # Django CLI management entrypoint
├── fintrack/                # Django project configuration module
│   ├── __init__.py
│   ├── settings.py          # Production & Dev configuration (includes MySQL setup)
│   ├── urls.py              # Root routing configuration
│   ├── wsgi.py              # WSGI server entrypoint
│   └── asgi.py              # ASGI server entrypoint
├── apps/                    # Sub-folder for all custom Django applications (modules)
│   └── __init__.py
├── static/                  # Project-wide static resources (Stitch UI assets)
│   ├── css/                 # Custom stylesheet files
│   ├── js/                  # Interactivity scripts
│   └── img/                 # Images & icons
└── templates/               # Global HTML templates directory
    └── base.html            # Main HTML layout wrapper with Bootstrap 5
```

---

## Prerequisites & Installation

### 1. Database Setup (MySQL)
Before running this application, you must set up your local MySQL server:
1. Open your MySQL command-line client or administration tool (e.g., MySQL Workbench).
2. Create the target database:
   ```sql
   CREATE DATABASE fintrack_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 2. Setting Up Virtual Environment & Dependencies
Navigate to the project root `fintrack` and perform the following:

#### Create Virtual Environment
```powershell
python -m venv venv
```

#### Activate Virtual Environment (Windows)
```powershell
venv\Scripts\activate
```

#### Install Dependencies
Make sure you have your MySQL development libraries installed on your machine so that `mysqlclient` can build properly.
```powershell
pip install -r requirements.txt
```

---

## Database Connection & Configuration

Database settings are defined in [settings.py](file:///c:/Users/hp/Documents/DAA/fintrack/fintrack/settings.py). 

For a production environment, you should create a `.env` file in the root directory to store database credentials securely:
```ini
DB_NAME=fintrack_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

---

## Commands Reference

### 1. Database Migrations
Create database schemas based on standard models (run these once MySQL database is running and configuration is aligned):
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 2. Creating a Superuser
Create an admin credential to access the Django backend:
```powershell
python manage.py createsuperuser
```

### 3. Run Development Server
Start the local server (defaults to port 8000):
```powershell
python manage.py runserver
```
The application will be accessible at: `http://127.0.0.1:8000/`
