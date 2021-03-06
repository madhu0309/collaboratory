from collab_app import models
from django import forms
from pagedown.widgets import PagedownWidget


class AnswerForm(forms.ModelForm):
    """AnswerForm definition."""

    answer_text = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = models.Answer
        fields = ("answer_text",)
        # label=mark_safe('my label<br />next line'

    # class Media:
    #     css = {
    #         'all': ('custom/stylesheets.css',)
    #     }
    #     js = ('custom/javascript.js',)

    def clean_answer_text(self):
        answer_text = self.cleaned_data.get("answer_text")
        if not answer_text or len(answer_text) < 3:
            raise forms.ValidationError("Please enter the answer!")
        return answer_text


class QuestionForm(forms.ModelForm):
    """Form definition for Question."""

    question_body = forms.CharField(widget=PagedownWidget())

    class Meta:
        """Meta definition for Questionform."""

        model = models.Question
        fields = ("question_title", "question_body")

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(
            *args, **kwargs
        )  # Call to ModelForm constructor
        self.fields["question_body"].widget.attrs["cols"] = 120
        self.fields["question_body"].widget.attrs["rows"] = 10
        # self.fields["question_body"].widget.attrs["row"] = 5
        # self.fields['long_desc'].widget.attrs['rows'] = 20
        # widgets = {
        #     "question_title": forms.TextInput(
        #         attrs={
        #             "style": "width: 400px",
        #             "class": "basicAutoComplete",
        #             "data-url": "/collab/",
        #         }
        #     ),
        # }


class CommentForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput, required=False)
    object_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    message = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": 2}))
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # comment_id = forms.IntegerField()

    class Meta:
        model = models.Comment
        fields = ("message",)

    def clean_message(self):
        message_text = self.cleaned_data.get("message", None)
        message_text = message_text.strip() if message_text else ""
        if not message_text or len(message_text) < 5:
            raise forms.ValidationError("Please enter the message!")
        return message_text


# class ReviewDataForm(ModelForm):
#     class Meta:
#         model = ReviewData
#         fields = '__all__'


#     def __init__(self, *args, **kwargs):
#         super(ReviewDataForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             if field in ['first_name', 'last_name']:
#                 self.fields[field].label = "Enter Your " + (' ').join(field.split('_'))
#                 self.fields[field].widget.attrs = {
#                     'class' : 'form-control',
#                     'placeholder': 'Enter your ' + (' ').join(field.split('_'))
#                 }
#             else:
#                 self.fields[field].label = "Enter Your " + field
#                 self.fields[field].widget.attrs = {
#                     'class' : 'form-control',
#                     'placeholder': 'Enter your ' + field
#                 }
