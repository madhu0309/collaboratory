from collab_app import models
from django import forms


class AnswerForm(forms.ModelForm):
    """AnswerForm definition."""

    class Meta:
        model = models.Answer
        fields = ("answer_text",)
        # label=mark_safe('my label<br />next line'

    def clean_answer_text(self):
        answer_text = self.cleaned_data.get("answer_text")
        if not answer_text or len(answer_text) < 3:
            raise forms.ValidationError("Please enter the answer!")
        return answer_text


class QuestionForm(forms.ModelForm):
    """Form definition for Question."""

    class Meta:
        """Meta definition for Questionform."""

        model = models.Question
        fields = ("question_title", "question_body")
        # widgets = {
        #     "question_title": forms.TextInput(
        #         attrs={
        #             "style": "width: 400px",
        #             "class": "basicAutoComplete",
        #             "data-url": "/collab/",
        #         }
        #     ),
        # }


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    message = forms.CharField(label="", widget=forms.Textarea)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # comment_id = forms.IntegerField()

    class Meta:
        model = models.Comment
        fields = ("message",)
