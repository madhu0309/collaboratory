from django.test import TestCase, Client
from collab_app.models import Question
from collab_app.models import Answer
from django.urls import reverse

# Create your tests here.


class QuestionTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_title="How to create models in django",
            question_body="I am a newbie to django and I want to learn django quickly.What are the best possible ways to learn django",
            # pub_date = ''
            # votes =
        )

    def test_question_listing(self):
        self.assertEqual(
            f"{self.question.question_title}", "How to create models in django"
        )
        self.assertEqual(
            f"{self.question.question_body}",
            "I am a newbie to django and I want to learn django quickly.What are the best possible ways to learn django",
        )
        # self.assertEqual(f'{self.question}')

    def test_question_list_view(self):
        response = self.client.get(reverse("collab_app:question-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How to create models in django")
        self.assertTemplateUsed(response, "collab_app/question_list.html")

