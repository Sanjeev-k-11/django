---
marp: true
theme: default
paginate: true
header: "StudyMate – Academic Progress & Study Planning Management System"
footer: "Confidential • College Project Presentation"
style: |
  section {
    font-family: 'Times New Roman', serif;
    background-color: #FFFDFB;
    color: #1F2937;
    padding: 40px 60px;
  }
  h1, h2, h3 {
    color: #9D174D;
    font-family: 'Times New Roman', serif;
  }
  footer {
    font-size: 12px;
    color: #6B7280;
  }
---

<!-- Slide 1: Title Slide -->
# 🎓 StudyMate
### Student Study Planning & Academic Progress Management System
**An All-in-One Academic Operating System for University Students**

- **Developer / Presenter:** Sanjeev Kumar
- **Technology Stack:** Python 3.14 • Django 6.1 • SQLite • Chart.js • FullCalendar • HTML5/CSS3
- **Repository:** [github.com/Sanjeev-k-11/django](https://github.com/Sanjeev-k-11/django)
- **Date:** Academic Year 2026

> *"Mastering academic excellence with structured clarity, cognitive habit formation, and data-driven progress."*

---

<!-- Slide 2: Problem Statement -->
# 📌 Problem Statement & Challenges

### The Modern Student's Dilemma
1. **Fragmented Workspaces:** Students juggle 4-6 apps daily (Google Calendar, Notion, WhatsApp, Timer apps, physical notebooks) leading to cognitive overload.
2. **Deadline Anxiety & Overdue Tasks:** Lack of centralized countdowns causes missed assignments and poor grade tracking.
3. **Distraction & Lack of Focus:** Long unguided study blocks lead to procrastination and burnout.
4. **Zero Longitudinal Insights:** Students have no visualization of actual study hours versus exam performance and GPA.

---

<!-- Slide 3: The Proposed Solution -->
# 💡 The Solution: StudyMate Academic OS

### A Unified, Purpose-Built Platform
- **Unified Academic Hub:** Courses, syllabus tasks, notes, exams, timetable, and study sessions connected in one database.
- **Scientific Habit Building:** Built-in 25/5 Pomodoro focus timer with automated session logging and streak preservation.
- **Proactive Visual Schedule:** FullCalendar-powered academic calendar linking assignments, tests, and deadlines.
- **Data-Driven Performance Analytics:** Real-time GPA projection, weekly study hour charts, and printable progress dossiers.

---

<!-- Slide 4: System Architecture & Technology Stack -->
# 🏗️ System Architecture & Technology Stack

```
   ┌─────────────────────────────────────────────────────────────┐
   │                  FRONTEND PRESENTATION TIER                 │
   │  Semantic HTML5 • Luxury Editorial CSS • Vanilla JavaScript │
   │  Chart.js 4.4 • FullCalendar 6.1 • FontAwesome 6 SVG Engine │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ HTTP / JSON AJAX
   ┌──────────────────────────────▼──────────────────────────────┐
   │                   APPLICATION SERVER TIER                   │
   │               Django 6.1.3 (Python 3.14 WSGI)               │
   │   • accounts  • core (Subjects/Tasks/Notes)  • planner      │
   │   • analytics (CSV/Report Generator)        • Django Admin  │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ ORM / SQL Queries
   ┌──────────────────────────────▼──────────────────────────────┐
   │                      DATABASE STORAGE                       │
   │            SQLite 3 (Relational Database Engine)            │
   │        User Isolation • Post-Save Signals • Migrations      │
   └─────────────────────────────────────────────────────────────┘
```

---

<!-- Slide 5: Core Modules & Features (1/2) -->
# 📦 Core Functional Modules (Part 1)

### 1. Course & Subject Tracking (`/subjects/`)
- Course code, instructor profile, target grade (e.g. `🎯 A`), and custom color tagging.
- Automated progress bars computing ratio of completed assignments per course.

### 2. Assignment & Subtask Checklists (`/assignments/`)
- Priority tags (`High`, `Medium`, `Low`) and real-time countdown chips (`Overdue`, `Due in 2 days`).
- Interactive AJAX checkbox toggles and dynamic subtask checklists.
- PDF/document attachment support for syllabus briefs.

### 3. Study Notes & Knowledge Base (`/notes/`)
- Categorized notes tagged by subject with pin-to-top prioritization.
- One-click print-ready styling and plain-text file download for offline review.

---

<!-- Slide 6: Core Modules & Features (2/2) -->
# 📦 Core Functional Modules (Part 2)

### 4. Interactive Pomodoro Study Timer (`/timer/`)
- Concentric luxury circular SVG progress ring with real-time percentage animation.
- Web Audio API ambient noise generator: **Rain**, **Deep Ocean Waves**, and **Clock Ticks**.
- Automatic session logging: saves duration directly to database and updates daily streak.

### 5. Academic Calendar & Timetable (`/calendar/`, `/timetable/`)
- FullCalendar view with event-type filters (Tasks, Exams, Goals, Reminders).
- Modal quick-inspector and weekly recurring class slot grid.

### 6. Exam Countdown & GPA Tracker (`/exams/`)
- Days-left countdown badge, syllabus revision notes, and exam room locator.
- Automated weighted GPA calculation on standard 4.0 scale.

---

<!-- Slide 7: Database Design & Entity Relationship -->
# 🗄️ Relational Database Schema

### Structured SQLite Entity Design
- **`User` & `Profile` (1:1):** Avatar, institution, grade, daily study goal hours.
- **`Subject` (1:N with User):** Color hex, course code, target grade, active/archived state.
- **`Assignment` (N:1 with Subject):** Priority, due date, status, file attachment.
- **`ChecklistItem` (N:1 with Assignment/Goal):** Subtasks with binary completion flag.
- **`StudySession` (N:1 with Subject):** Duration in minutes, start timestamp, focus notes.
- **`Exam` (N:1 with Subject):** Date, total marks, obtained marks, letter grade, GPA.
- **`TimetableEntry` & `Reminder`:** Day-of-week slots and alert timestamps.

> **Integrity & Security:** Full multi-tenant data isolation; queries filter strictly by `request.user`.

---

<!-- Slide 8: Technical Innovations & UX Highlights -->
# ✨ Technical Highlights & Innovations

1. **Client-Side Audio Synthesis:**
   - No heavy `.mp3` dependencies; generates soothing focus frequencies in real-time via the browser's native `AudioContext`.
2. **Instant AJAX Toggling:**
   - Tasks and subtasks update asynchronously with CSRF protection without page reloads.
3. **Luxury Editorial UI System:**
   - Bespoke styling matching modern luxury publications (`Times New Roman`, rose/gold gradients, squircle icon badges, dark mode toggle).
4. **Robust Admin Portal:**
   - Custom-branded Django administration with color swatches, progress bars, and CSV export.

---

<!-- Slide 9: Security, Authentication & Robustness -->
# 🔒 Security & Architecture Standards

- **Flexible Multi-Identifier Login:**
  - Authenticate using either **Username** OR **Email Address** seamlessly.
- **CSRF & XSS Hardening:**
  - Django middleware token validation on all POST/AJAX endpoints.
- **Role-Based Permission Separation:**
  - Student views strictly scoped to owner records; superuser controls restricted to Django Admin.
- **Password Validation & Hashing:**
  - PBKDF2 with SHA-256 password hashing.
- **Automated Test Suite:**
  - 100% passing test coverage verifying models, authentication, streak calculation, and CSV generation.

---

<!-- Slide 10: Live Project Demonstration & Credentials -->
# 🖥️ Live Demonstration & Credentials

### Local Deployment
- **Local Application URL:** `http://127.0.0.1:8000/`
- **Django Administration:** `http://127.0.0.1:8000/admin/`

### Pre-Seeded Accounts for Testing

| Role | Username / Email | Password | Pre-loaded Data |
|---|---|---|---|
| **Demo Student** | `demo` / `rahul.demo@studymate.edu` | `password123` | 4 Courses, 8 Tasks, 6 Sessions (6-Day Streak 🔥), 3 Exams |
| **Administrator** | `admin` / `admin@studentstay.com` | `password123` | Full superuser database access with custom luxury portal |

---

<!-- Slide 11: Future Roadmap & Scalability -->
# 🚀 Future Scope & Enhancements

1. **AI-Powered Syllabus Parsing:**
   - Upload course syllabus PDF to automatically extract assignment dates and generate weekly study milestones via LLM.
2. **Collaborative Virtual Study Rooms:**
   - Peer Pomodoro synchronization with shared study room timers.
3. **Native Mobile App (React Native / Flutter):**
   - Push notifications for upcoming deadlines and lock-screen study widgets.
4. **Third-Party Calendar Sync:**
   - Two-way synchronization with Google Calendar, Outlook, and Apple iCal.

---

<!-- Slide 12: Conclusion & Q&A -->
# 🎯 Conclusion & Key Takeaways

### Summary
- StudyMate successfully bridges the gap between **academic planning** and **day-to-day focus execution**.
- Built with production-grade Django best practices, modern interactive JavaScript, and an elegant visual design.
- Ready for deployment, evaluation, and real-world student adoption.

### Thank You!
**Questions & Answers**  
- **GitHub Repository:** [github.com/Sanjeev-k-11/django](https://github.com/Sanjeev-k-11/django)
- **Live Server:** `http://127.0.0.1:8000/`
