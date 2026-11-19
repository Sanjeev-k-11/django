from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from django.utils import timezone

from core.models import Subject, Assignment, StudyGoal, Note, ChecklistItem
from planner.models import StudySession, Exam
from planner.utils import get_user_streak, get_study_time_summary


class StudyMateTestCase(TestCase):
    def setUp(self):
        # Create User A
        self.user_a = User.objects.create_user(username='usera', password='password123', email='a@example.com')
        # Create User B
        self.user_b = User.objects.create_user(username='userb', password='password123', email='b@example.com')

        # Subject for User A
        self.sub_a = Subject.objects.create(
            user=self.user_a,
            name="Physics 101",
            code="PHY101",
            color="#2563EB"
        )

        # Subject for User B
        self.sub_b = Subject.objects.create(
            user=self.user_b,
            name="Chemistry 101",
            code="CHEM101",
            color="#0D9488"
        )

        # Assignment for User A
        self.assign_a = Assignment.objects.create(
            user=self.user_a,
            subject=self.sub_a,
            title="Lab Report 1",
            due_date=date.today() + timedelta(days=2),
            priority="high",
            status="not_started"
        )

        # Note for User A
        self.note_a = Note.objects.create(
            user=self.user_a,
            subject=self.sub_a,
            title="Kinematics Notes",
            content="v = u + at"
        )

        self.client_a = Client()
        self.client_a.login(username='usera', password='password123')

        self.client_b = Client()
        self.client_b.login(username='userb', password='password123')

    def test_user_profile_creation(self):
        """Test signal automatically created profiles."""
        self.assertIsNotNone(self.user_a.profile)
        self.assertEqual(self.user_a.profile.daily_study_target_hours, 4.0)

    def test_user_isolation_subjects(self):
        """User B should receive 404 when trying to view User A's subject."""
        response = self.client_b.get(reverse('core:subject_detail', kwargs={'pk': self.sub_a.pk}))
        self.assertEqual(response.status_code, 404)

        # User A can view own subject
        response_a = self.client_a.get(reverse('core:subject_detail', kwargs={'pk': self.sub_a.pk}))
        self.assertEqual(response_a.status_code, 200)

    def test_user_isolation_assignments(self):
        """User B should receive 404 when trying to view or edit User A's assignment."""
        response = self.client_b.get(reverse('core:assignment_detail', kwargs={'pk': self.assign_a.pk}))
        self.assertEqual(response.status_code, 404)

        response_a = self.client_a.get(reverse('core:assignment_detail', kwargs={'pk': self.assign_a.pk}))
        self.assertEqual(response_a.status_code, 200)

    def test_assignment_ajax_toggle(self):
        """Test AJAX toggle for assignment completion."""
        url = reverse('core:assignment_toggle_status', kwargs={'pk': self.assign_a.pk})
        response = self.client_a.post(url)
        self.assertEqual(response.status_code, 200)
        self.assign_a.refresh_from_db()
        self.assertEqual(self.assign_a.status, 'completed')
        self.assertIsNotNone(self.assign_a.completed_at)

        # Toggle back to pending
        response2 = self.client_a.post(url)
        self.assertEqual(response2.status_code, 200)
        self.assign_a.refresh_from_db()
        self.assertEqual(self.assign_a.status, 'not_started')

    def test_study_session_and_streak(self):
        """Test logging study session and streak calculation."""
        today = date.today()
        # Log session today
        StudySession.objects.create(
            user=self.user_a,
            subject=self.sub_a,
            start=timezone.now(),
            duration_minutes=50
        )
        # Log session yesterday
        StudySession.objects.create(
            user=self.user_a,
            subject=self.sub_a,
            start=timezone.now() - timedelta(days=1),
            duration_minutes=45
        )

        streak = get_user_streak(self.user_a)
        self.assertEqual(streak, 2)

        summary = get_study_time_summary(self.user_a)
        self.assertGreater(summary['today_minutes'], 0)

    def test_dashboard_view(self):
        """Test dashboard view loads properly for logged in user."""
        response = self.client_a.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Physics 101")

    def test_export_csv_views(self):
        """Test CSV export endpoints return valid CSV headers and content."""
        response = self.client_a.get(reverse('analytics:export_assignments_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Lab Report 1', response.content.decode())
