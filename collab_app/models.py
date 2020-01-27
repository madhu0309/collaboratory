from django.db import models
from django.urls import reverse
from collab_app.utils import unique_slug_generator
from django.db.models.signals import pre_save

# Create your models here.


class Question(models.Model):
    question_title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    question_body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.question_title[:10]

    def get_absolute_url(self):
        return reverse("question-detail", kwargs={"slug": self.slug})

    # def get_absolute_url(self):
    #     return reverse("question-detail", args=[str(self.id)])

    def get_question_body(self):
        return self.question_body[:50]


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Question)


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="question_answer",
    )
    answer_text = models.TextField()
    votes = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.answer_text[:30]
