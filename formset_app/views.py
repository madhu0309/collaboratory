from django.shortcuts import render, redirect
from django.forms import modelformset_factory, inlineformset_factory
from .models import Programmer, Language

# Create your views here.


# def index(request):
#     InfoFormSet = modelformset_factory(
#         Info, fields=("name", "location"), extra=2, can_delete=True
#     )

#     if request.method == "POST":
#         form = InfoFormSet(request.POST)
#         # instances = form.save(commit=False)

#         # for instance in instances:
#         #     instance.save()

#         form.save()

#     form = InfoFormSet()  # queryset=Info.objects.none())
#     return render(request, "index.html", {"formset": form})


def progview(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    # LanguageFormset = modelformset_factory(Language, fields=("name",),)
    LanguageFormset = inlineformset_factory(
        Programmer, Language, fields=("name",), can_delete=False, extra=2, max_num=6
    )

    if request.method == "POST":
        # formset = LanguageFormset(
        #     request.POST, queryset=Language.objects.filter(programmer_id=programmer.id)
        # )
        formset = LanguageFormset(request.POST, instance=programmer)
        if formset.is_valid():
            formset.save()
            # for instance in instances:
            #     instance.programmer_id = programmer.id
            #     instance.save()
            # instances.save()

            return redirect("prog", programmer_id=programmer.id)

    # formset = LanguageFormset(
    #     queryset=Language.objects.filter(programmer_id=programmer.id)
    # )
    formset = LanguageFormset(instance=programmer)
    return render(request, "prog.html", {"formset": formset})


# def manage_albums(request):
#     AlbumFormSet = modelformset_factory(
#         Album, can_order=True, can_delete=True, fields=["artist", "name", "release",]
#     )
#     if request.method == "POST":
#         formset = AlbumFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             for form in formset.ordered_forms:
#                 form.instance.order = form.cleaned_data["ORDER"]
#             formset.save()
#             messages.success(request, u"Formset edited successfully.")
#             return HttpResponseRedirect(reverse("formsets"))
#         else:
#             messages.error(request, u"Please correct the errors below.")

#     else:
#         formset = AlbumFormSet(queryset=Album.objects.order_by("order"))
#     return render(request, "formset_app/manage_album.html", {"formset": formset})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookFormset, BookModelFormset
from .models import Book


def create_book_model_form(request):
    template_name = "formset_app/create_normal.html"
    heading_message = "Model Formset Demo"
    if request.method == "GET":
        formset = BookModelFormset(queryset=Book.objects.none())
    elif request.method == "POST":
        formset = BookModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
                if form.cleaned_data.get("name"):
                    form.save()
            return HttpResponse("<h1>It worked not as expected</h1>")

    return render(
        request, template_name, {"formset": formset, "heading": heading_message,}
    )
