from django.test import TestCase, Client
from collab_app.models import Question, Answer
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
        self.answer = Answer.objects.create(
            question=self.question,
            answer_text="Try to learn Documentation thorougly it will be very helpfull for beginners and start with function based views",
            # comment="Thank you for your reply",
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

    def test_question_detail_view(self):
        response = self.client.get(self.question.get_absolute_url())
        no_response = self.client.get("/detail/How to create models in django/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "How to create models in django")
        self.assertContains(
            response,
            "I am a newbie to django and I want to learn django quickly.What are the best possible ways to learn django",
        )
        self.assertContains(
            response,
            "Try to learn Documentation thorougly it will be very helpfull for beginners and start with function based views",
        )
        # self.assertContains(
        #     response, "Thank you for your reply",
        # )
        self.assertTemplateUsed(response, "collab_app/question_detail.html")

