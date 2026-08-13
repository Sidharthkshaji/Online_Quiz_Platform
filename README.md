# 🎓 Online Quiz Platform

A robust, full-featured web application built with **Flask**, **MySQL**, **SQLAlchemy**, and **Bootstrap**. Designed for educational institutions and interview preparation, this platform allows students to take timed quizzes with automated scoring, while administrators can manage categories, quizzes, questions, and view platform metrics.

---

## 🌟 Features

### 👨‍🎓 Student Features
* **Quiz Catalog:** Browse available quizzes filtered by categories and difficulty levels.
* **Timed Quiz Engine:** Take interactive quizzes with real-time countdown timers and automatic submission upon expiration.
* **Question Navigation:** Easily move between questions with answer state persistence.
* **Instant Evaluation & Results:** Get immediate feedback on overall score, percentage, time spent, and performance status.
* **Detailed Attempt Review:** Review completed quizzes to see selected answers vs. correct options.
* **Student Dashboard:** Track personal test history, average score metrics, and completed quizzes.

### 🛠️ Admin Features
* **Category Management:** Full CRUD operations for organizing quizzes into distinct subjects/topics.
* **Quiz Management:** Create and edit quizzes with customizable time limits, difficulty settings, and category assignments.
* **Question & Choice Bank:** Manage multiple-choice questions (MCQs), set marks, dynamic choices, and designated correct options.
* **Quiz Preview:** Inspect full quizzes with answer keys prior to student availability.
* **Admin Dashboard:** Overview of total users, active quizzes, total attempts, and system analytics.

### 🔐 Security & System Architecture
* **Role-Based Access Control (RBAC):** Distinct route permissions for `student` and `admin` roles using `Flask-Login`.
* **Server-Side Security:** Server-validated quiz completion timers to prevent client-side time manipulation.
* **Password Hashing:** Secure password storage using Werkzeug security functions.
* **Database Migration System:** Database version control using `Flask-Migrate` (Alembic).

---

## 🛠️ Tech Stack

* **Backend Framework:** Python 3, Flask (Application Factory & Blueprints Pattern)
* **Database & ORM:** MySQL, Flask-SQLAlchemy, PyMySQL
* **Database Migrations:** Flask-Migrate (Alembic)
* **Forms & Validation:** Flask-WTF, WTForms
* **Authentication:** Flask-Login
* **Environment Configuration:** `python-dotenv`
* **Frontend:** HTML5, CSS3, JavaScript (Dynamic Timer & Navigation), Bootstrap / Jinja2 Templates

---

## 📂 Project Structure

```text
OnlineQuizPlatform/
├── .env                     # Environment configuration variables
└── Online_Quiz_Platform/
    ├── run.py               # Main application entry point
    ├── requirements.txt     # Python project dependencies
    ├── migrations/          # Database migration scripts (Flask-Migrate)
    └── app/                 # Modular Flask Application Package
        ├── __init__.py      # App factory initialization & Blueprint registration
        ├── config.py        # Database & app configuration settings
        ├── extensions.py    # Flask extension instances (db, login_manager, migrate)
        ├── forms/           # WTForms definitions (login, registration, quiz, question, category)
        ├── models/          # SQLAlchemy database models
        │   ├── user.py      # User model (Student/Admin roles)
        │   ├── category.py  # Quiz categories
        │   ├── quiz.py      # Quiz entity
        │   ├── question.py  # Question entity
        │   ├── choice.py    # Multiple choice options
        │   ├── attempt.py   # Quiz attempt records
        │   └── response.py  # Individual user responses per question
        ├── routes/          # Blueprint route controllers
        │   ├── auth.py      # Authentication (login, register, logout)
        │   ├── admin.py     # Admin management endpoints
        │   ├── student.py   # Student quiz execution & review endpoints
        │   └── main.py      # General landing & dashboard routes
        ├── services/        # Business logic & database operations layer
        ├── static/          # Static assets (CSS, JS, images)
        └── templates/       # Jinja2 HTML templates
            ├── admin/       # Admin views (categories, quizzes, questions)
            ├── auth/        # Login & registration views
            ├── dashboard/   # Admin & Student dashboards
            ├── student/     # Quiz taking, results, and review views
            └── base.html    # Master HTML template layout
```

---

## 📊 Database Schema Summary

| Entity | Description | Key Relationships |
| :--- | :--- | :--- |
| **User** | Stores user credentials, profile name, and role (`student` / `admin`). | One-to-many with `Quiz` (as creator), `Attempt`. |
| **Category** | Topic categorization for quizzes. | One-to-many with `Quiz`. |
| **Quiz** | Holds quiz configuration (title, time limit, difficulty, category). | Belongs to `Category`, has many `Question`, `Attempt`. |
| **Question** | MCQ items assigned to a quiz with specific mark values. | Belongs to `Quiz`, has many `Choice`, `Response`. |
| **Choice** | Possible answer options for a question with `is_correct` boolean indicator. | Belongs to `Question`. |
| **Attempt** | Track student quiz attempt (start time, submit time, score, status). | Belongs to `User` and `Quiz`, has many `Response`. |
| **Response** | Student choice selection per question during an attempt. | Belongs to `Attempt`, `Question`, and `Choice`. |

---

## ⚡ Quick Start & Setup Guide

### 1. Prerequisites
* **Python 3.8+**
* **MySQL Server** (running locally or remotely)
* **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/OnlineQuizPlatform.git
cd OnlineQuizPlatform/Online_Quiz_Platform
```

### 3. Create & Activate Virtual Environment
* **Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Setup (`.env`)
Create a `.env` file in the project root (or update the existing `.env` file) with your database and app credentials:

```env
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_PORT=3306
DB_NAME=online_quiz_db
DB_USER=root
DB_PASSWORD=your_mysql_password
```

> **Note:** Ensure the MySQL database specified in `DB_NAME` (e.g., `online_quiz_db`) is created in your MySQL server before running migrations.

```sql
CREATE DATABASE online_quiz_db;
```

### 6. Database Migrations
Initialize and apply database migrations to build tables:

```bash
flask db upgrade
```

### 7. Run the Application
Start the Flask development server:

```bash
python run.py
```

The application will be accessible at: **`http://127.0.0.1:5000`**

---

## 🚀 Workflow Overview

1. **Register / Login:** Register a new user account or log in.
2. **Admin Portal:**
   - Log in with an Admin account.
   - Navigate to `/admin/categories` to add quiz topics (e.g., Logical Reasoning, Quantitative Aptitude, Technical).
   - Navigate to `/admin/quizzes` to create a quiz, specify difficulty, category, and time limit.
   - Add questions and options under `/admin/quizzes/<quiz_id>/questions`.
3. **Student Portal:**
   - Log in with a Student account.
   - Browse quizzes at `/student/quizzes`.
   - Start a quiz to trigger the countdown timer and question view.
   - Submit answers or let the timer auto-submit.
   - View instant results and detailed attempt feedback.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
