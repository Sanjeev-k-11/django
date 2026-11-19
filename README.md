# StudyMate – Student Study Planning & Academic Progress Management System

StudyMate is a production-quality, modern, full-stack Django web application engineered to help students streamline course management, track deadlines, monitor study habits, log Pomodoro focus sessions, and measure academic progress through an intelligent analytics dashboard.

---

## 🌟 Highlights & Key Features

### 1. 🎓 Courses & Subject Management
- Full CRUD for enrolled subjects with color picker, instructor contact, and target grade.
- Archive / restore subjects.
- Subject detail view showing aggregated tasks, goals, notes, exams, timetable slots, and total study hours logged.

### 2. 📝 Assignments, Subtasks & Deadlines
- Assignment tracking with priority tags (`High`, `Medium`, `Low`), status (`Not Started`, `In Progress`, `Completed`), and due date/time countdowns.
- Subtask checklists with live AJAX checkoff and progress bar updates.
- One-click AJAX "Mark as done" toggle (instant updates without page refresh).
- Color-coded badges: Overdue (Red), Due within 2 days (Amber), Completed (Green).
- Resource file attachment upload and download (PDFs, docs, lab guides).
- Filter by subject, status, priority, and sort options.

### 3. 🎯 Study Goals & Milestones
- Categorized into **Daily**, **Weekly**, and **Long-term** goals.
- Interactive live progress slider (0% to 100%) with automated status updates.

### 4. 📚 Study Notes & Knowledge Base
- Card grid preview with tags, subject filters, and keyword search.
- Pin important notes to the top of your revision dashboard.
- Print-optimized view for study sheets and one-click download as plain-text `.txt`.

### 5. ⏱️ Pomodoro Study Timer
- Customizable 25/5 Pomodoro focus timer (Focus, Short Break, Long Break).
- Subject selection and study notes logging.
- Automatically saves completed sessions to the database.
- Real-time study streak calculation and today's / this week's hours summary.

### 6. 📅 FullCalendar Academic Schedule
- Full month, week, and list views.
- Color-coded event markers for assignments, exams, study goals, and reminders.
- Direct click-through to event details.

### 7. 🗓️ Weekly Timetable Grid
- 7-day recurring class grid (Monday to Sunday) styled with subject theme colors.
- "Today's Classes" widget on the smart home dashboard.

### 8. 🏆 Exams, GPA & Performance Tracker
- Exam schedule with countdowns ("12 days left", "Exam Today!").
- Post-exam marks entry with automatic percentage and letter grade calculation (`A+`, `A`, `B`, `C`, `D`, `F`).
- Estimated 4.0 GPA calculator and subject performance charts.

### 9. 📊 Analytics, Reports & CSV Data Export
- Weekly and monthly study hours breakdown.
- Subject-wise study time distribution (Chart.js pie chart).
- Task and goal completion rates.
- Exam performance trend line chart.
- Export assignments and study sessions to CSV.
- Formal, printable academic progress report.

### 10. 🎨 UI / UX Excellence
- Clean, modern, light white aesthetic with `"Times New Roman", Times, serif` typography throughout all pages, inputs, tables, and charts.
- Dark mode toggle with persistent `localStorage` preference.
- Notification bell dropdown tracking overdue tasks, upcoming deadlines, and exams.
- Keyboard shortcut: press **`N`** anywhere to open the Quick Add modal.
- Fully responsive layout with mobile drawer and bottom navigation bar.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.14, Django 6.1.3, SQLite3
- **Media & Images**: Pillow 13.0.0
- **Frontend**: HTML5, Django Template Language, Custom CSS with CSS variables, Vanilla JavaScript
- **Libraries & CDNs**:
  - Chart.js 4.4.2
  - FullCalendar 6.1.11
  - FontAwesome 6.5.1

---

## 📁 Project Structure

```
django/
├── manage.py
├── requirements.txt
├── README.md
├── PROJECT_DOCS.md
├── db.sqlite3
├── studymate_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py         # Profile (avatar, target hours, institution)
│   ├── forms.py          # User registration, login, profile edit
│   ├── views.py          # Auth, profile, password change/reset
│   ├── signals.py        # Automated profile generation
│   ├── urls.py
│   └── admin.py
├── core/
│   ├── models.py         # Subject, Assignment, Goal, Note, ChecklistItem
│   ├── forms.py          # SubjectForm, AssignmentForm, GoalForm, NoteForm
│   ├── views.py          # Dashboard, CRUD views, AJAX endpoints, search
│   ├── views_errors.py   # Custom 404 & 500 handlers
│   ├── context_processors.py # Notifications badge counter & due items
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py          # Unit tests (models, isolation, views)
│   └── management/
│       └── commands/
│           └── seed_demo.py # Realistic demo data seeder
├── planner/
│   ├── models.py         # StudySession, Exam, TimetableEntry, Reminder
│   ├── forms.py          # StudySessionForm, ExamForm, TimetableEntryForm
│   ├── views.py          # Timer, FullCalendar API, Timetable, Exams
│   ├── utils.py          # Study streak & time calculation routines
│   ├── urls.py
│   └── admin.py
├── analytics/
│   ├── views.py          # Analytics dashboard, CSV exports, progress report
│   └── urls.py
├── static/
│   ├── css/
│   │   └── style.css     # CSS variables, Times New Roman font, themes
│   └── js/
│       ├── main.js       # Dark mode, AJAX, hotkeys, modals
│       └── timer.js      # Pomodoro audio, countdown, session logging
└── templates/
    ├── base.html
    ├── partials/         # Sidebar, topbar, navbar, quick add modal
    ├── accounts/         # Login, register, profile, password reset
    ├── core/             # Dashboard, subjects, assignments, goals, notes
    ├── planner/          # Pomodoro timer, calendar, timetable, exams
    ├── analytics/        # Reports, charts, printable progress page
    └── errors/           # Custom 404 & 500 error templates
```

---

## 🚀 Quickstart & Setup Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
```bash
python manage.py migrate
```

### 3. Seed Realistic Demo Data
```bash
python manage.py seed_demo
```

### 4. Run Automated Test Suite
```bash
python manage.py test
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000** in your browser.

---

## 🔑 Login Credentials

### 1. 🛡️ Django Admin Superuser (Full Database Access)
Access all database models, user accounts, and academic records via the Django Admin Portal:
- **Admin URL:** **http://127.0.0.1:8000/admin/**
- **Username:** `admin` *(or email: `admin@studentstay.com`)*
- **Password:** `password123`
- **Role:** Superuser / Staff with full permissions to create, edit, inspect, and delete all SQLite database records.

---

### 2. 🎓 Demo Student Account (Student Dashboard Access)
Access the frontend StudyMate app as a student:
- **App Login URL:** **http://127.0.0.1:8000/accounts/login/**
- **Username:** `demo` *(or email: `rahul.demo@studymate.edu`)*
- **Password:** `password123`
- **Student Name:** Rahul Sharma (Stanford University)
- **Active Streak:** 6-Day Study Streak 🔥
- **Preloaded Data:** 4 Subjects, 8 Assignments, 4 Goals, 5 Notes, 6 Study Sessions, 3 Exams, Timetable & Reminders

