from collab_app import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AnswerForm(forms.ModelForm):
    """AnswerForm definition."""
    class Meta:
        model = models.Answer
        fields = ('answer_text',)

    def clean_answer_text(self):
        answer_text = self.cleaned_data.get('answer_text')
        if not answer_text or len(answer_text) < 3:
            raise forms.ValidationError("Please enter the answer!")
        return answer_text


class QuestionForm(forms.ModelForm):
    """Form definition for Question."""

    class Meta:
        """Meta definition for Questionform."""

        model = models.Question
        fields = ('question_title', 'question_body')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

