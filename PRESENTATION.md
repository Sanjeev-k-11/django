---
marp: true
theme: default
paginate: true
header: "StudyMate – Student Study Planning & Academic Progress Management System"
footer: "Academic Project Presentation • Department of Computer Science & Engineering"
style: |
  section {
    font-family: 'Times New Roman', serif;
    background-color: #FFFDFB;
    color: #1F2937;
    padding: 35px 55px;
  }
  h1 {
    color: #9D174D;
    font-size: 1.85rem;
    font-family: 'Times New Roman', serif;
    margin-bottom: 0.6rem;
  }
  h2, h3 {
    color: #831843;
    font-family: 'Times New Roman', serif;
  }
  table {
    font-size: 0.82rem;
    width: 100%;
    border-collapse: collapse;
  }
  th {
    background-color: #FFF1F2;
    color: #9D174D;
    padding: 8px 10px;
    border: 1px solid #FECDD3;
  }
  td {
    padding: 7px 10px;
    border: 1px solid #E5E7EB;
  }
  footer {
    font-size: 11px;
    color: #6B7280;
  }
  code {
    background-color: #F3F4F6;
    color: #9D174D;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 0.85em;
  }
---

<!-- Slide 1: Title Slide -->
# 🎓 StudyMate
### Student Study Planning & Academic Progress Management System
**A Production-Ready Academic Operating System for Higher Education**

### 👥 Project Team Members:
1. **Ayush Kumar** — Reg. No: `12322101`
2. **Sanjeev Kumar Yadav** — Reg. No: `12321575`
3. **Amit Yadav** — Reg. No: `12300923`

- **Domain:** Web Application Engineering / EdTech
- **Technology Stack:** Python 3.14 • Django 6.1.3 • SQLite • Chart.js • FullCalendar • HTML5/CSS3
- **Source Code Repository:** [github.com/Sanjeev-k-11/django](https://github.com/Sanjeev-k-11/django)
- **Academic Year:** 2026

> *"Mastering academic journey with disciplined habit formation, structured clarity, and data-driven progress."*

---

<!-- Slide 2: Project Overview & Motivation -->
# 📖 Project Overview & Motivation

### Why StudyMate?
- **Cognitive Science Foundation:** Research shows that combining **spaced retrieval**, **timeboxing (Pomodoro)**, and **streak gamification** improves student retention by over **40%**.
- **Fragmentation in Current Education:**
  - Modern students use one app for to-dos, another for timers, a spreadsheet for GPA, and messy notebooks for syllabus notes.
  - Context switching causes decision fatigue, forgotten deadlines, and academic stress.
- **StudyMate's Mission:**
  - Build a single, zero-distraction, unified web environment where a student plans their semester, logs study blocks, tracks upcoming exams, computes GPA, and visualizes weekly output.

---

<!-- Slide 3: Problem Statement -->
# 📌 Problem Statement & Challenges

```
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│        EXISTING PROBLEMS         │        │       STUDYMATE SOLUTIONS        │
├──────────────────────────────────┤        ├──────────────────────────────────┤
│ 1. Missed Deadlines & Anxiety    │ ──────>│ Automated Countdown & Due Chips  │
│ 2. Distracted Study Sessions     │ ──────>│ Concentric SVG Pomodoro + Audio  │
│ 3. Fragmented Course Materials   │ ──────>│ Subject-Linked Notes & Tasks     │
│ 4. No GPA Visibility             │ ──────>│ Automated 4.0 GPA Calculator     │
│ 5. Cluttered, Ad-Heavy Apps      │ ──────>│ Luxury Editorial, Clean White UI │
└──────────────────────────────────┘        └──────────────────────────────────┘
```

- **Target Audience:** College undergraduates, graduate researchers, high school scholars, and competitive exam aspirants.

---

<!-- Slide 4: Competitive Analysis -->
# 📊 Competitive Analysis & Market Comparison

| Feature / Capability | StudyMate | Notion | Google Calendar | Forest App | Quizlet |
|---|:---:|:---:|:---:|:---:|:---:|
| **Course & Subject Binding** | ✅ Yes | ⚠️ Manual DB | ❌ No | ❌ No | ❌ No |
| **Integrated Pomodoro Timer** | ✅ Built-in | ❌ Plugin req. | ❌ No | ✅ Paid | ❌ No |
| **Built-in Ambient Audio (WebAudio)** | ✅ Rain/Waves | ❌ No | ❌ No | ⚠️ Paid Sound | ❌ No |
| **Automated GPA & Grade Projection** | ✅ Built-in | ⚠️ Complex Formula | ❌ No | ❌ No | ❌ No |
| **Academic Calendar with Filters** | ✅ FullCalendar | ⚠️ Basic | ✅ Standard | ❌ No | ❌ No |
| **Subtask AJAX Checklist** | ✅ Real-time | ✅ Yes | ❌ Basic | ❌ No | ❌ No |
| **Self-Hosted / SQLite Privacy** | ✅ 100% Private | ❌ Cloud only | ❌ Cloud only | ❌ Cloud only | ❌ Cloud only |

---

<!-- Slide 5: System Architecture -->
# 🏗️ System Architecture & Layered Design

```
+-----------------------------------------------------------------------------------+
|                           PRESENTATION LAYER (CLIENT)                             |
|    HTML5 Semantic DOM • Times New Roman Editorial Design • Dark/Light Modes       |
|    FontAwesome 6 SVG Vector Engine • Chart.js 4.4 • FullCalendar 6.1 • Web Audio  |
+------------------------------------------+----------------------------------------+
                                           | HTTP Requests / JSON AJAX
+------------------------------------------v----------------------------------------+
|                          APPLICATION LAYER (DJANGO 6.1.3)                         |
|   • core: Subjects, StudyGoals, Assignments, Subtasks, Notes, Global Search       |
|   • planner: StudySession Timer, FullCalendar Events API, Exams, Timetable        |
|   • accounts: Multi-identifier Auth (Email/Username), Profile, Signals, Avatars  |
|   • analytics: Chart Data Generators, CSV Exporters, Printable Progress Reports  |
|   • admin: Custom Luxury Django Database Administration Portal                    |
+------------------------------------------+----------------------------------------+
                                           | Django ORM / Parameterized SQL
+------------------------------------------v----------------------------------------+
|                              DATABASE LAYER (SQLITE 3)                            |
|       Relational Tables • Foreign Key Cascades • Normalized Schema Design        |
+-----------------------------------------------------------------------------------+
```

---

<!-- Slide 6: Functional Modules – Academics -->
# 📚 Core Functional Modules: Academics

### 1. Course Management (`/subjects/`)
- Course code (e.g. `CS-301`), instructor name, target grade (`🎯 A`), and custom color badge.
- Real-time completion progress bar computed dynamically from completed assignments.

### 2. Assignment & Task Tracking (`/assignments/`)
- Priority tags (`High`, `Medium`, `Low`) with countdown chips (`Overdue`, `Due in 2 days`).
- Subtask checklists with asynchronous AJAX toggles (persists without page refresh).
- Syllabus brief file upload and document attachment support.

### 3. Study Notes & Knowledge Repository (`/notes/`)
- Rich text study notes categorized by subject and tagged for searchability.
- Priority "Pin to Top" flag, dedicated print view, and plain-text file download.

---

<!-- Slide 7: Functional Modules – Planning & Productivity -->
# ⏱️ Core Functional Modules: Planning & Habits

### 1. Pomodoro Focus Timer (`/timer/`)
- SVG concentric circular progress ring with dynamic stroke animation.
- Presets: **15m Sprint**, **25m Classic**, **50m Deep Work**, **90m Flow State**.
- Built-in **Web Audio Focus Synthesizer**: Generates gentle pink rain noise, deep brown ocean frequencies, and clock ticks without external audio files.
- Completed session auto-logging linked directly to course and notes.

### 2. Academic Calendar (`/calendar/`)
- FullCalendar integration with client-side event filtering (`All`, `Tasks`, `Exams`, `Goals`, `Reminders`).
- Interactive modal popover showing event timing, priority, and direct edit link.

### 3. Weekly Timetable Grid (`/timetable/`)
- 7-day recurring class schedule grid with room numbers and subject color badges.

---

<!-- Slide 8: Functional Modules – Analytics & Exams -->
# 📈 Core Functional Modules: Exams & Analytics

### 1. Exam Schedules & GPA Calculator (`/exams/`)
- Countdown counter (`⏳ In 5 days`), syllabus revision notes, and exam hall locator.
- Automated grade mapping (`A`, `B`, `C`, `F`) and weighted GPA projection on a 4.0 scale.

### 2. Smart Visual Analytics (`/analytics/`)
- **Chart.js Bar Chart:** Daily study hours logged over the last 7 days.
- **Chart.js Doughnut Chart:** Study time distribution across enrolled courses.
- **Weekly Study Target Gauge:** Compares actual hours against user daily target.

### 3. Reporting & Data Exports
- One-click CSV export for all assignments and study sessions.
- Printable academic progress dossier with summary metrics and signature blocks.

---

<!-- Slide 9: Relational Database Schema (ER Model) -->
# 🗄️ Relational Database Schema & Data Models

```
┌──────────────────┐         1:1         ┌────────────────────────┐
│    auth_user     │────────────────────>│    accounts_profile    │
│  id, username,   │                     │  institution, avatar,  │
│  email, password │                     │  daily_target_hours    │
└────────┬─────────┘                     └────────────────────────┘
         │ 1:N
         ├───────────────────────────────────────────┬──────────────────────┐
         ▼ 1:N                                       ▼ 1:N                  ▼ 1:N
┌──────────────────┐     1:N     ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   core_subject   │────────────>│ core_assignment  │  │ core_studygoal   │  │ planner_exam     │
│  name, code,     │             │  title, due_date │  │  target_date,    │  │  date, marks,    │
│  color, grade    │             │  status, priority│  │  progress, type  │  │  grade, location │
└────────┬─────────┘             └────────┬─────────┘  └────────┬─────────┘  └──────────────────┘
         │ 1:N                            │ 1:N                 │ 1:N
         ├────────────────────────┐       └──────────┬──────────┘
         ▼ 1:N                    ▼ 1:N              ▼
┌──────────────────┐     ┌──────────────────┐  ┌──────────────────┐
│ planner_session  │     │    core_note     │  │core_checklistitem│
│ duration_minutes,│     │  title, content, │  │  title, is_done, │
│ start, notes     │     │  tags, is_pinned │  │  created_at      │
└──────────────────┘     └──────────────────┘  └──────────────────┘
```

---

<!-- Slide 10: Key Algorithms & Formulas -->
# 🧮 Key Algorithms & Mathematical Formulas

### 1. Consecutive Study Streak Calculation (`planner/utils.py`)
Counts unbroken consecutive calendar days with at least one logged study session:
$$\text{Streak} = \max \{ k \mid \forall i \in [0, k-1], \, \text{HasSession}(\text{Today} - i \cdot \text{days}) = \text{True} \}$$
*Handles timezone normalization and treats missing days as streak breakers.*

### 2. Weighted Grade Point Average (GPA) Formula (`planner/models.py`)
$$\text{GPA} = \frac{\sum_{i=1}^{N} (\text{GradePoint}_i \times \text{Credits}_i)}{\sum_{i=1}^{N} \text{Credits}_i}$$
- Grade Points: $A = 4.0, \, B = 3.0, \, C = 2.0, \, D = 1.0, \, F = 0.0$.

### 3. Pomodoro Dynamic Ring Offset
$$\text{StrokeOffset} = \text{Circumference} \times \left(1 - \frac{\text{TimeRemaining}}{\text{TotalSeconds}}\right)$$

---

<!-- Slide 11: Implementation Highlights & Code Quality -->
# 💻 Technical Implementation Highlights

### 1. Flexible Multi-Identifier Authentication (`accounts/forms.py`)
Users can log in using either their **Username** OR their **Email address**:
```python
user = User.objects.filter(models.Q(username__iexact=identifier) | models.Q(email__iexact=identifier)).first()
if user and user.check_password(password):
    login(request, user)
```

### 2. Client-Side Web Audio Noise Synthesis (`static/js/timer.js`)
Zero external `.mp3` dependencies; real-time audio buffer synthesis:
```javascript
const buffer = ambientCtx.createBuffer(1, bufferSize, ambientCtx.sampleRate);
const data = buffer.getChannelData(0);
for (let i = 0; i < bufferSize; i++) {
    lastOut = (lastOut + (0.02 * (Math.random() * 2 - 1))) / 1.02;
    data[i] = lastOut * 3.5; // Smooth Brownian wave frequency
}
```

---

<!-- Slide 12: UI/UX Design System -->
# 🎨 UI/UX Design System & Luxury Editorial Theme

### Design Philosophy (Inspired by High-End Editorial Aesthetics)
- **Typography:** Classic, authoritative `"Times New Roman", Times, serif` throughout all headings, prose, buttons, and tables.
- **Color Palette:**
  - Ambient Cream / Warm White: `#FFFBF7` & `#FFFFFF`
  - Luxury Velvet Rose Accent: `#9D174D` & `#BE185D`
  - Royal Warm Amber / Gold: `#D97706` & `#FEF3C7`
- **Micro-Interactions:**
  - Squircle Icon Badges (52px rounded squircle containers with soft drop shadows).
  - Card lift on hover (`transform: translateY(-4px)` with shadow bloom).
  - Concentric pulsing rings on active timers.
- **Accessibility:** Full Light / Dark theme toggle with CSS variable propagation.

---

<!-- Slide 13: Software Development Life Cycle (SDLC) -->
# 🔄 SDLC & Agile Development Roadmap

```
  SPRINT 1 (Foundation)     SPRINT 2 (Academics)      SPRINT 3 (Planner)
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│ • Project setup       │ │ • Subject CRUD        │ │ • Pomodoro Timer      │
│ • SQLite Schema & Auth│ │ • Assignment & Subtasks│ │ • FullCalendar API   │
│ • Profile Signals     │ │ • Notes Repository    │ │ • Exam Schedules      │
└───────────┬───────────┘ └───────────┬───────────┘ └───────────┬───────────┘
            │                         │                         │
            ▼                         ▼                         ▼
  SPRINT 4 (Analytics)      SPRINT 5 (UI Luxury)      SPRINT 6 (Verification)
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│ • Chart.js Metrics    │ │ • Editorial UI Redesign│ │ • Automated Test Suite│
│ • Streak Algorithms   │ │ • Squircle Icon Badges│ │ • 100% Pass Verification│
│ • CSV/Report Export   │ │ • Web Audio Synthesis │ │ • GitHub Versioning   │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
```

---

<!-- Slide 14: Quality Assurance & Testing Matrix -->
# 🧪 Quality Assurance & Test Verification Matrix

### Automated Test Suite (`python manage.py test`) — 100% Pass Rate

| Test ID | Module Tested | Test Scenario | Expected Outcome | Status |
|:---:|:---|:---|:---|:---:|
| **TC-01** | `accounts` | User Registration & Profile Signal | Profile automatically created with default targets | ✅ PASS |
| **TC-02** | `accounts` | Multi-Identifier Login | Allows login via email as well as username | ✅ PASS |
| **TC-03** | `core` | User Query Isolation | User A cannot view or edit User B's subjects | ✅ PASS |
| **TC-04** | `core` | AJAX Task Status Toggle | Asynchronously toggles completion status | ✅ PASS |
| **TC-05** | `planner` | Consecutive Streak Counter | Correctly calculates 6 consecutive study days | ✅ PASS |
| **TC-06** | `planner` | GPA Calculation | Weighted average maps letter grades accurately | ✅ PASS |
| **TC-07** | `analytics`| CSV Exporter | Generates well-formed CSV file with HTTP 200 | ✅ PASS |

---

<!-- Slide 15: Security & Data Privacy -->
# 🛡️ Security, Privacy & Data Integrity

1. **CSRF Protection:**
   - Every state-changing form and AJAX request validates Django's `X-CSRFToken` header.
2. **SQL Injection Prevention:**
   - 100% of database interactions leverage Django ORM's parameterized query builder.
3. **Cross-Site Scripting (XSS) Mitigation:**
   - Automatic HTML template escaping enabled across all views.
4. **Data Isolation (Multi-Tenancy):**
   - Every query filters strictly by `request.user`:
     `Assignment.objects.filter(user=request.user)`.
5. **Secure Local Storage:**
   - Full data resides in `db.sqlite3` with zero third-party tracking or cloud vendor lock-in.

---

<!-- Slide 16: System Requirements & Specifications -->
# ⚙️ Hardware & Software Specifications

### Client System Requirements
- **Web Browser:** Modern browser (Chrome 110+, Firefox 115+, Safari 16+, Edge).
- **Audio Support:** HTML5 Web Audio API capable for focus noise generator.
- **Display Resolution:** Responsive (Optimized for Mobile 375px up to 4K Desktop).

### Server & Development Environment
- **Operating System:** Windows 10/11, macOS, or Linux (Ubuntu 22.04+).
- **Runtime:** Python 3.14+ (or Python 3.10+).
- **Framework:** Django 6.1.3.
- **Database:** SQLite 3 (Built-in zero-configuration relational database).
- **Memory & Storage:** Min 512 MB RAM, < 100 MB disk space.

---

<!-- Slide 17: Demonstration & Preloaded Data -->
# 🖥️ Live Demonstration & Demo Accounts

### Local Server URL
- **Student Portal:** `http://127.0.0.1:8000/`
- **Database Admin:** `http://127.0.0.1:8000/admin/`

### Ready-to-Test Accounts

| Account Role | Username | Password | Preloaded Academic Data |
|---|---|---|---|
| **Student (Demo)** | `demo` *(or `rahul.demo@studymate.edu`)* | `password123` | • 4 Subjects (CS, Math, Physics, Eng)<br>• 8 Tasks (Subtasks & Deadlines)<br>• 6 Study Sessions (6-Day Streak 🔥)<br>• 3 Exams with GPA & Room schedules |
| **Superuser (Admin)** | `admin` *(or `admin@studentstay.com`)* | `password123` | • Complete SQLite database oversight<br>• Custom luxury admin theme<br>• Color-coded badges & inlines |

---

<!-- Slide 18: Future Roadmap & Scaling Strategy -->
# 🚀 Future Roadmap & Scaling Strategy

1. **AI-Powered Syllabus Parsing (LLM Ingestion):**
   - Upload course syllabus PDFs; AI extracts deadlines, exam dates, and generates an automated 14-week study roadmap.
2. **Peer Study Rooms (WebSockets / Django Channels):**
   - Synchronized virtual study rooms where classmates study together with shared Pomodoro intervals.
3. **Native Mobile App (Flutter / React Native):**
   - Offline-first mobile app with home-screen Pomodoro widgets and lock-screen push notifications.
4. **Third-Party Calendar Integration:**
   - Two-way `.ics` calendar sync with Google Calendar, Microsoft Outlook, and Apple iCal.

---

<!-- Slide 19: Conclusion & Project Summary -->
# 🎯 Conclusion & Key Takeaways

### Project Impact
- **Comprehensive Academic Solution:** StudyMate eliminates academic disorganization by unifying courses, tasks, notes, focus cycles, and grades into a single high-performance web hub.
- **Production Engineering Standards:** Built strictly following Django's modular architecture, PEP-8 guidelines, semantic HTML, and responsive mobile-first styling.
- **Practical Engineering Value:** Demonstrates mastery in full-stack web engineering, relational database design, client-side audio APIs, asynchronous DOM manipulation, and automated testing.

---

<!-- Slide 20: Thank You & Project Team -->
# 🙏 Thank You!

### 👥 Project Team Members:
- **Ayush Kumar** — Reg. No: `12322101`
- **Sanjeev Kumar Yadav** — Reg. No: `12321575`
- **Amit Yadav** — Reg. No: `12300923`

---

### 🌐 Live Links & Project Assets:
- **GitHub Repository:** [github.com/Sanjeev-k-11/django](https://github.com/Sanjeev-k-11/django)
- **Live Local Server:** `http://127.0.0.1:8000/`
- **Admin Database Portal:** `http://127.0.0.1:8000/admin/`

> *"Education is not the learning of facts, but the training of the mind to think." — Albert Einstein*
