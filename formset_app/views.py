from django.shortcuts import render, redirect
from django.forms import modelformset_factory, inlineformset_factory
from .models import Info, Programmer, Language

# Create your views here.


def index(request):
    InfoFormSet = modelformset_factory(
        Info, fields=("name", "location"), extra=2, can_delete=True
    )

    if request.method == "POST":
        form = InfoFormSet(request.POST)
        # instances = form.save(commit=False)

        # for instance in instances:
        #     instance.save()

        instances = form.save()

    form = InfoFormSet()  # queryset=Info.objects.none())
    return render(request, "index.html", {"Formset": form})


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

