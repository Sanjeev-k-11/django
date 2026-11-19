# StudyMate – Student Study Planning & Academic Progress Management System
## Complete Project Documentation & Progress Log

> **Project Name:** StudyMate  
> **Status:** Production-Ready & Actively Running  
> **Architecture:** Full-stack Django (Python 3.14 + Django 6.1.3 + SQLite)  
> **UI/UX Philosophy:** Luxury, editorial, clean white & ambient warm palette, Times New Roman typography, rounded squircle card grids, hero carousel slider, WhatsApp floating support pill, dark mode support.

---

## 1. Project Overview & Objectives
StudyMate is a comprehensive student study planning and academic progress management system combining:
- **Public Luxury Showcase & Landing Page (`/`)**:
  - Top navigation with monogram emblem badge, pill links, search pill, and authentication actions.
  - Interactive Hero Carousel Slider with tag badges, editorial headings, prose, slider arrows, and animated dot indicators.
  - "Study By Category" Academic Pillars grid with squircle pastel icon badges and `Browse →` rose pill buttons.
  - Real-time statistics counters, student review cards, call-to-action banner, and luxury footer.
  - Floating WhatsApp Chat / Academic Support pill with quick assistance.
- **About Us Page (`/about/`)**:
  - StudyMate vision, student frustration to academic mastery story, 4 cognitive values, 3-step academic flywheel.
- **Support & Contact Page (`/contact/`)**:
  - Direct WhatsApp support card, academic help desk email, interactive FAQ accordion.
- **Course & Subject Tracking (`/subjects/`)**:
  - Color-coded subjects, syllabus goals, progress indicators, and total study hours.
- **Assignment & Deadline Management (`/assignments/`)**:
  - Real-time subtask checklists, status toggles via AJAX, overdue and upcoming countdowns, file attachments.
- **Study Goal Setting (`/goals/`)**:
  - Short-term and long-term goal setting with interactive progress sliders.
- **Knowledge Base (`/notes/`)**:
  - Categorized, tagged, and pinned notes with print view and plain-text export.
- **Interactive Pomodoro Study Timer (`/timer/`)**:
  - Built-in 25/5 min focus timer with subject logging and automatic study session tracking.
- **Timetable & Calendar (`/timetable/`, `/calendar/`)**:
  - Weekly recurring class schedule grid and interactive FullCalendar integration.
- **Exams & Academic Performance (`/exams/`)**:
  - Exam countdowns, grade calculators, and GPA metrics.
- **Smart Analytics & Visual Dashboard (`/analytics/`, `/dashboard/`)**:
  - Chart.js charts, study streak calculation, time-of-day greetings, and CSV/PDF export.

---

## 2. Tech Stack & Dependencies
- **Backend**: Python 3.14, Django 6.1.3, SQLite3
- **Image Processing**: Pillow 13.0.0
- **Frontend**:
  - HTML5 & Django Template Language (DTL)
  - Custom CSS3 with CSS variables (Light & Dark themes + Luxury Rose/Warm Palette)
  - Typography: `"Times New Roman", Times, serif` across the entire app
  - Vanilla JavaScript (ES6+) for carousel auto-play, interactive timers, AJAX requests, and modals
  - Chart.js (CDN) for interactive analytics
  - FullCalendar (CDN) for academic calendar views
  - FontAwesome 6 (CDN) for icons

---

## 3. Database Models & Schema
- **Profile**: `user` (OneToOne), `avatar`, `institution`, `course_grade`, `daily_study_target_hours`, `bio`.
- **Subject**: `user`, `name`, `code`, `teacher`, `color`, `target_grade`, `is_archived`.
- **StudyGoal**: `user`, `subject`, `title`, `description`, `target_date`, `goal_type`, `status`, `progress`.
- **Assignment**: `user`, `subject`, `title`, `description`, `due_date`, `due_time`, `priority`, `status`, `completed_at`, `attachment`.
- **ChecklistItem**: `assignment`/`goal`, `title`, `is_done`.
- **Note**: `user`, `subject`, `title`, `content`, `tags`, `is_pinned`.
- **StudySession**: `user`, `subject`, `start`, `duration_minutes`, `notes`.
- **Exam**: `user`, `subject`, `title`, `date`, `time`, `location`, `syllabus_notes`, `marks_obtained`, `total_marks`.
- **TimetableEntry**: `user`, `subject`, `day_of_week`, `start_time`, `end_time`, `room`.
- **Reminder**: `user`, `title`, `datetime`, `is_done`.

---

## 4. Demo Account Credentials
- **URL:** `http://127.0.0.1:8000`
- **Username:** `demo`
- **Password:** `password123`
- **Student Name:** Rahul Sharma
- **Institution:** Stanford University
- **Study Streak:** 6-Day Study Streak 🔥
- **Admin Panel:** `http://127.0.0.1:8000/admin/`
