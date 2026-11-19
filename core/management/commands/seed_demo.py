from datetime import date, datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import Profile
from core.models import Subject, StudyGoal, Assignment, ChecklistItem, Note
from planner.models import StudySession, Exam, TimetableEntry, Reminder


class Command(BaseCommand):
    help = "Seed demo student data for StudyMate application"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding demo data for StudyMate..."))

        # 1. Create or get demo user
        user, created = User.objects.get_or_create(username="demo")
        user.first_name = "Rahul"
        user.last_name = "Sharma"
        user.email = "rahul.demo@studymate.edu"
        user.set_password("password123")
        user.save()

        # Update profile
        profile = user.profile
        profile.institution = "Stanford University"
        profile.course_grade = "B.S. Computer Science (Junior Year)"
        profile.daily_study_target_hours = 4.0
        profile.bio = "Passionate student interested in Algorithms, Distributed Systems, and Quantum Computing. Aiming for Dean's Honors List."
        profile.save()

        self.stdout.write(self.style.SUCCESS(f"User '{user.username}' created/updated."))

        # Clear previous demo items for clean state
        Subject.objects.filter(user=user).delete()
        StudySession.objects.filter(user=user).delete()
        Exam.objects.filter(user=user).delete()
        TimetableEntry.objects.filter(user=user).delete()
        Reminder.objects.filter(user=user).delete()

        today = date.today()

        # 2. Create 4 Subjects
        s1 = Subject.objects.create(
            user=user,
            name="Data Structures & Algorithms",
            code="CS101",
            teacher="Dr. Alan Turing",
            color="#2563EB",
            target_grade="A+",
        )
        s2 = Subject.objects.create(
            user=user,
            name="Calculus & Linear Algebra",
            code="MATH201",
            teacher="Prof. Katherine Johnson",
            color="#0D9488",
            target_grade="A",
        )
        s3 = Subject.objects.create(
            user=user,
            name="Modern Physics & Quantum Mechanics",
            code="PHYS301",
            teacher="Dr. Richard Feynman",
            color="#7C3AED",
            target_grade="A",
        )
        s4 = Subject.objects.create(
            user=user,
            name="Technical Writing & Academic English",
            code="ENG105",
            teacher="Prof. Virginia Woolf",
            color="#F59E0B",
            target_grade="A+",
        )

        self.stdout.write(self.style.SUCCESS("4 Subjects created."))

        # 3. Create 8 Assignments
        a1 = Assignment.objects.create(
            user=user, subject=s1,
            title="Balanced Binary Search Tree Implementation",
            description="Implement AVL tree insertions, deletions, and self-balancing rotations in Python or C++. Write unit tests.",
            due_date=today + timedelta(days=2),
            due_time=datetime.strptime("23:59", "%H:%M").time(),
            priority="high",
            status="in_progress",
        )
        ChecklistItem.objects.create(assignment=a1, title="Implement Left & Right Rotations", is_done=True)
        ChecklistItem.objects.create(assignment=a1, title="Handle Double Rotation Cases (LR / RL)", is_done=True)
        ChecklistItem.objects.create(assignment=a1, title="Write unit tests for 1000 random insertions", is_done=False)

        a2 = Assignment.objects.create(
            user=user, subject=s2,
            title="Eigenvalues & Diagonalization Problem Set",
            description="Complete textbook problems 4.1 to 4.15 from Chapter 4 on Matrix Eigenvectors.",
            due_date=today + timedelta(days=1),
            due_time=datetime.strptime("17:00", "%H:%M").time(),
            priority="medium",
            status="not_started",
        )
        ChecklistItem.objects.create(assignment=a2, title="Calculate characteristic polynomial roots", is_done=False)
        ChecklistItem.objects.create(assignment=a2, title="Verify orthogonal eigenvectors", is_done=False)

        a3 = Assignment.objects.create(
            user=user, subject=s3,
            title="Schrödinger Wave Equation Lab Simulation",
            description="Simulate a 1D particle in an infinite potential well using Python matplotlib.",
            due_date=today - timedelta(days=2),  # Overdue
            due_time=datetime.strptime("18:00", "%H:%M").time(),
            priority="high",
            status="in_progress",
        )
        ChecklistItem.objects.create(assignment=a3, title="Set boundary condition equations", is_done=True)
        ChecklistItem.objects.create(assignment=a3, title="Plot wave probability density", is_done=False)

        a4 = Assignment.objects.create(
            user=user, subject=s4,
            title="Research Paper Literature Review Draft",
            description="Write a 1500-word draft reviewing recent advancements in quantum error correction.",
            due_date=today + timedelta(days=5),
            priority="medium",
            status="not_started",
        )

        a5 = Assignment.objects.create(
            user=user, subject=s1,
            title="Dijkstra's Shortest Path Algorithm Lab",
            description="Build graph representation with adjacency lists and benchmark Dijkstra using min-heaps.",
            due_date=today - timedelta(days=5),
            priority="high",
            status="completed",
            completed_at=timezone.now() - timedelta(days=5),
        )
        ChecklistItem.objects.create(assignment=a5, title="Create Graph class", is_done=True)
        ChecklistItem.objects.create(assignment=a5, title="Benchmark execution time", is_done=True)

        a6 = Assignment.objects.create(
            user=user, subject=s2,
            title="Multivariable Integration Homework 3",
            description="Calculate double and triple integrals in cylindrical and spherical coordinates.",
            due_date=today - timedelta(days=8),
            priority="low",
            status="completed",
            completed_at=timezone.now() - timedelta(days=8),
        )

        a7 = Assignment.objects.create(
            user=user, subject=s3,
            title="Photoelectric Effect & Planck's Constant Lab Report",
            description="Format experimental measurements, calculate work function, and derive Planck's constant.",
            due_date=today + timedelta(days=9),
            priority="low",
            status="not_started",
        )

        a8 = Assignment.objects.create(
            user=user, subject=s4,
            title="Oral Technical Presentation Slides",
            description="Prepare 10 presentation slides explaining Transformer attention mechanisms to peer students.",
            due_date=today + timedelta(days=4),
            priority="medium",
            status="in_progress",
        )

        self.stdout.write(self.style.SUCCESS("8 Assignments created."))

        # 4. Create 4 Goals
        StudyGoal.objects.create(
            user=user, subject=s1,
            title="Master Dynamic Programming & Graph Traversals",
            description="Solve 25 classic DP and BFS/DFS problems on LeetCode before the midterm exam.",
            target_date=today + timedelta(days=14),
            goal_type="weekly",
            status="in_progress",
            progress=65,
        )
        StudyGoal.objects.create(
            user=user, subject=s2,
            title="Review Vector Calculus & Stokes' Theorem",
            description="Read chapter 8 and re-solve all lecture practice questions.",
            target_date=today + timedelta(days=7),
            goal_type="weekly",
            status="in_progress",
            progress=40,
        )
        StudyGoal.objects.create(
            user=user, subject=s3,
            title="Daily Modern Physics Formula Revision",
            description="Review quantum operators and de Broglie relations for 30 minutes every morning.",
            target_date=today + timedelta(days=1),
            goal_type="daily",
            status="pending",
            progress=20,
        )
        StudyGoal.objects.create(
            user=user,
            title="Achieve Semester GPA of 3.8 or Higher",
            description="Maintain consistent study streak and submit every assignment at least 24 hours early.",
            target_date=today + timedelta(days=60),
            goal_type="long_term",
            status="in_progress",
            progress=75,
        )

        self.stdout.write(self.style.SUCCESS("4 Goals created."))

        # 5. Create 5 Notes
        Note.objects.create(
            user=user, subject=s1,
            title="Graph Algorithms Quick Cheat Sheet",
            content="""# Graph Representation & Traversal

1. BFS (Breadth-First Search)
   - Uses Queue (FIFO)
   - Guarantees shortest path in unweighted graphs
   - Time Complexity: O(V + E)

2. DFS (Depth-First Search)
   - Uses Stack / Recursion
   - Ideal for cycle detection and topological sorting
   - Time Complexity: O(V + E)

3. Dijkstra's Algorithm
   - Single-source shortest path with non-negative weights
   - Min-heap priority queue gives O((V + E) log V)""",
            tags="algorithms, graphs, cheat-sheet, exam-prep",
            is_pinned=True,
        )

        Note.objects.create(
            user=user, subject=s2,
            title="Fundamental Theorems of Vector Calculus",
            content="""Gradient Theorem:
Integrals along curves depend only on endpoints.

Green's Theorem:
Connects line integral around simple closed curve C to double integral over plane region D.

Divergence Theorem (Gauss):
Flux of vector field through closed surface equals volume integral of its divergence.

Stokes' Theorem:
Circulation around closed boundary curve equals surface integral of curl.""",
            tags="math, calculus, formulas, midterm",
            is_pinned=True,
        )

        Note.objects.create(
            user=user, subject=s3,
            title="Quantum Mechanics Operators & Commutators",
            content="""Position operator: x_hat = x
Momentum operator: p_hat = -i * h_bar * d/dx
Energy operator (Hamiltonian): H_hat = -(h_bar^2 / 2m) * d^2/dx^2 + V(x)

Canonical Commutation Relation:
[x_hat, p_hat] = i * h_bar
Implies Heisenberg's Uncertainty Principle: Delta_x * Delta_p >= h_bar / 2.""",
            tags="physics, quantum, operators, exam",
            is_pinned=False,
        )

        Note.objects.create(
            user=user, subject=s4,
            title="Academic Writing Best Practices & Style",
            content="""1. Precision over verbosity: use active voice where appropriate.
2. Structure: Abstract -> Introduction -> Related Work -> Methodology -> Results -> Conclusion.
3. Cite sources properly using IEEE or APA formats.
4. Always proofread for subject-verb agreement and logical transitions.""",
            tags="writing, english, academic, report",
            is_pinned=False,
        )

        Note.objects.create(
            user=user, subject=s1,
            title="Time Complexity Reference Table (Big-O)",
            content="""Array: Access O(1), Search O(n), Insert/Delete O(n)
Binary Search Tree: Average O(log n), Worst O(n)
AVL / Red-Black Tree: O(log n) guaranteed
Hash Map: Average O(1), Worst O(n)
Merge Sort: O(n log n)
Quick Sort: Average O(n log n), Worst O(n^2)
Heap Sort: O(n log n)""",
            tags="algorithms, big-o, complexity, quick-ref",
            is_pinned=False,
        )

        self.stdout.write(self.style.SUCCESS("5 Notes created."))

        # 6. Create 6 Study Sessions (Consecutive 6 days streak)
        sessions_data = [
            (today, 50, s1, "Solved LeetCode graph problems and reviewed AVL trees"),
            (today - timedelta(days=1), 45, s2, "Calculated surface integrals and solved homework 3"),
            (today - timedelta(days=2), 60, s3, "Derived 1D Schrödinger equation wave functions"),
            (today - timedelta(days=3), 40, s1, "Implemented min-heap for Dijkstra algorithm"),
            (today - timedelta(days=4), 30, s4, "Drafted literature review introduction"),
            (today - timedelta(days=5), 55, s2, "Studied matrix diagonalization and eigenvalues"),
        ]

        for s_date, dur, sub, notes in sessions_data:
            StudySession.objects.create(
                user=user,
                subject=sub,
                start=timezone.now().replace(year=s_date.year, month=s_date.month, day=s_date.day, hour=15, minute=0),
                duration_minutes=dur,
                notes=notes,
            )

        self.stdout.write(self.style.SUCCESS("6 Study Sessions created (6-day streak active)."))

        # 7. Create 3 Exams
        Exam.objects.create(
            user=user, subject=s1,
            title="Midterm Assessment - Data Structures",
            date=today - timedelta(days=10),
            time=datetime.strptime("10:00", "%H:%M").time(),
            location="Gates Computer Science Hall 101",
            syllabus_notes="Arrays, Linked Lists, Stacks, Queues, Binary Trees, and Hash Tables.",
            marks_obtained=94.5,
            total_marks=100.0,
        )

        Exam.objects.create(
            user=user, subject=s2,
            title="Calculus II Mid-Semester Exam",
            date=today + timedelta(days=4),
            time=datetime.strptime("14:00", "%H:%M").time(),
            location="Math Building Auditorium B",
            syllabus_notes="Eigenvalues, diagonal matrices, Green's & Stokes' theorem. Scientific calculators allowed.",
        )

        Exam.objects.create(
            user=user, subject=s3,
            title="Modern Physics Comprehensive Quiz",
            date=today + timedelta(days=12),
            time=datetime.strptime("11:30", "%H:%M").time(),
            location="Science Center Room 304",
            syllabus_notes="Wave-particle duality, uncertainty principle, potential barrier tunneling.",
        )

        self.stdout.write(self.style.SUCCESS("3 Exams created."))

        # 8. Create Timetable Entries (Mon - Fri)
        TimetableEntry.objects.create(
            user=user, subject=s1, day_of_week=0,  # Monday
            start_time=datetime.strptime("09:00", "%H:%M").time(),
            end_time=datetime.strptime("10:30", "%H:%M").time(),
            room="CS Lab 204",
        )
        TimetableEntry.objects.create(
            user=user, subject=s2, day_of_week=0,  # Monday
            start_time=datetime.strptime("11:00", "%H:%M").time(),
            end_time=datetime.strptime("12:30", "%H:%M").time(),
            room="Math Hall A",
        )
        TimetableEntry.objects.create(
            user=user, subject=s3, day_of_week=1,  # Tuesday
            start_time=datetime.strptime("10:00", "%H:%M").time(),
            end_time=datetime.strptime("11:30", "%H:%M").time(),
            room="Physics Lecture 1",
        )
        TimetableEntry.objects.create(
            user=user, subject=s4, day_of_week=1,  # Tuesday
            start_time=datetime.strptime("13:00", "%H:%M").time(),
            end_time=datetime.strptime("14:30", "%H:%M").time(),
            room="Humanities 102",
        )
        TimetableEntry.objects.create(
            user=user, subject=s1, day_of_week=2,  # Wednesday
            start_time=datetime.strptime("09:00", "%H:%M").time(),
            end_time=datetime.strptime("10:30", "%H:%M").time(),
            room="CS Lab 204",
        )
        TimetableEntry.objects.create(
            user=user, subject=s2, day_of_week=3,  # Thursday
            start_time=datetime.strptime("11:00", "%H:%M").time(),
            end_time=datetime.strptime("12:30", "%H:%M").time(),
            room="Math Hall A",
        )
        TimetableEntry.objects.create(
            user=user, subject=s3, day_of_week=4,  # Friday
            start_time=datetime.strptime("14:00", "%H:%M").time(),
            end_time=datetime.strptime("16:00", "%H:%M").time(),
            room="Physics Experimental Lab",
        )

        self.stdout.write(self.style.SUCCESS("Timetable entries created."))

        # 9. Create Reminders
        Reminder.objects.create(
            user=user,
            title="Return Calculus textbook to Central Library",
            datetime=timezone.now() + timedelta(days=1),
            is_done=False,
        )
        Reminder.objects.create(
            user=user,
            title="Attend Office Hours with Dr. Turing for Tree questions",
            datetime=timezone.now() + timedelta(days=2),
            is_done=False,
        )
        Reminder.objects.create(
            user=user,
            title="Submit Spring Semester Scholarship Application",
            datetime=timezone.now() + timedelta(days=5),
            is_done=False,
        )

        self.stdout.write(self.style.SUCCESS("Reminders created."))
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Demo database successfully seeded!"))
        self.stdout.write(self.style.SUCCESS("Login credentials: Username: 'demo' | Password: 'password123'"))
        self.stdout.write(self.style.SUCCESS("=================================================="))
