import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question=question_text, pub_date=date)

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_date(self):
        """
        was_published_recently() should return false if date is in the future
        """
        future_date = timezone.now() + datetime.timedelta(days=10)
        future_question = Question(pub_date=future_date)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_date(self):
        """
        was_published_recently() should return false if pub_date is older than 24 hours from now
        """
        old_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_date)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_date(self):
        """
        was_published_recently() should return true if pub_date is within 24 hours from now
        """
        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_date)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions present, display appropriate message
        """
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No polls are available")
        self.assertQuerySetEqual(
            resp.context["latest_question_list"], []
        )

    def test_past_questions(self):
        """
        Questions with past date are shown on the index page
        """
        question = create_question(question_text="Test past question?", days=-10)
        resp = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            resp.context["latest_question_list"], [question]
        )
    
    def test_past_and_future_questions(self):
        """
        Even if past and future questions exist, only past questions are shown
        """
        question = create_question("Past question test?", days=-5)
        create_question("Future question?", days=5)
        resp = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            resp.context["latest_question_list"], [question]
        )
    
    def test_multiple_past_questions(self):
        """
        The index page should display multiple questions
        """
        q1 = create_question("Test question 1?", days=-2)
        q2 = create_question("Test question 2?", days=-3)
        resp = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            resp.context["latest_question_list"], [q1, q2]
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of an unpublished question should return 404
        """
        future_question = create_question("Test future question?", days=10)
        url = reverse("polls:detail", args=(future_question.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a past question should display question text
        """
        question = create_question("Test past question?", days=-1)
        url = reverse("polls:detail", args=(question.id,))
        resp = self.client.get(url)
        self.assertContains(resp, question.question)
