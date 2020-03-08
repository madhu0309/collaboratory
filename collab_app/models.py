from django.db import models
from django.urls import reverse
from django.conf import settings
from collab_app.utils import unique_slug_generator
from django.db.models.signals import pre_save
from users.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext as _
from six import python_2_unicode_compatible
from vote.models import VoteModel
from hitcount.models import HitCountMixin, HitCount

# Create your models here.


@python_2_unicode_compatible
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = (
            super(CommentManager, self)
            .filter(content_type=content_type, object_id=obj_id)
            .filter(parent=None)
        )
        return qs


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("User")
    )
    message = models.TextField(max_length=1500, verbose_name=_("Message"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Parent comment"),
        # related_name="children",
    )
    is_approved = models.BooleanField(default=True, verbose_name=_("Is approved"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = CommentManager()

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return self.message[:20]

    def children(self):
        return Comment.objects.filter(parent=self)

    # return self.objects.filter(parent=self)
    @property
    def is_parent(self):
        """Return 'True' if instance is a parent."""
        if self.parent is not None:
            return False
        return True


class Question(VoteModel, models.Model):
    question_title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    question_body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    # votes = models.IntegerField(default=0, blank=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True
    )
    comments = GenericRelation(Comment, related_query_name="question")
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )

    def __str__(self):
        return self.question_title[:10]

    # def get_absolute_url(self):
    #     return reverse("collab_app:question-detail", kwargs={"slug": self.slug})
    # @property
    # def get_absolute_url(self):
    #     return reverse("question-detail", args=[str(self.id)])

    def get_question_body(self):
        return self.question_body[:50]

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


# for comment in Comment.objects.all():
# ...     if comment.is_parent:
# ...         print(comment.message)
# ...     else:
# ...         print(comment.children.all().first())


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Question)


class Answer(VoteModel, models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="question_answer",
    )
    answer_text = models.TextField()
    # votes = models.IntegerField(default=0, blank=True)
    comments = GenericRelation(Comment, related_query_name="answer")

    def __str__(self):
        return self.answer_text[:30]

    # commented_by = models.ForeignKey(
    #     get_user_model(), on_delete=models.CASCADE, null=True
    # )
