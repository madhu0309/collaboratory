from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from .models import Book, Author


class BookForm(forms.Form):
    name = forms.CharField(
        label="Book Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Book Name here"}
        ),
    )


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("name",)
        labels = {"name": "Book Name", "isbn_number": "ISBN Number"}
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Book Name here"}
            )
        }


BookFormset = formset_factory(BookForm)
BookModelFormset = modelformset_factory(
    Book,
    fields=("name", "isbn_number"),
    extra=1,
    can_delete=True,
    widgets={
        "name": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Book Name here"}
        ),
        "isbn_number": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter isbn number"}
        ),
    },
)


AuthorFormset = modelformset_factory(
    Author,
    fields=("name",),
    extra=1,
    widgets={
        "name": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Author Name here"}
        )
    },
)


class AuthorInlineForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ()


AuthorInlineFormset = inlineformset_factory(
    Book,
    Author,
    form=AuthorInlineForm,
    fields=("name",),
    can_delete=True,
    extra=1,
    # max_num=6,
    widgets={
        "name": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Author Name here"}
        )
    },
)
