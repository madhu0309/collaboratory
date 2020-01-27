from django.shortcuts import get_object_or_404, redirect, render
from collab_app.models import Question
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from collab_app.forms import QuestionForm, AnswerForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# from django.utils import json

# from dal import autocomplete

# from haystack.generic_views import SearchView
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import logout, authenticate, login
# from collab_app.forms import NewUserForm
# Create your views here.
import os


class QuestionListView(ListView):
    model = Question
    context_object_name = "question_list"
    template_name = "collab_app/question_list.html"
    paginate_by = 2

    # def get_queryset(self): # new
    #     if self.request.GET.get('q') != None:
    #         query = self.request.GET.get('q')
    #         return Question.objects.filter(
    #             Q(question_title__icontains=query) #| Q(author__icontains=query)
    #         )
    #     else:
    #         return Question.objects.all()

    def get_context_data(self, **kwargs):
        # search_key =
        context = super(QuestionListView, self).get_context_data(**kwargs)

        if self.request.GET.get("q") != None:
            query = self.request.GET.get("q")
            list_exam = Question.objects.filter(
                Q(question_title__icontains=query)  # | Q(author__icontains=query)
            )
        else:
            list_exam = Question.objects.all()
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_exams"] = file_exams
        if self.request.GET.get("q") != None:
            context["search"] = self.request.GET.get("q")
        return context


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get("term", "").capitalize()
        search_qs = Question.objects.filter(question_title__startswith=q)
        results = []
        # print q
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


class QuestionDetailView(FormView, DetailView):
    model = Question
    form_class = AnswerForm
    template_name = "collab_app/question_detail.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        print(self)
        print(context)
        if "slug" in self.kwargs:
            context["object"] = get_object_or_404(Question, slug=self.kwargs["slug"])
        context["form"] = self.get_form()
        return context

    def form_valid(self, form):
        print("+++++++++++++++++")
        print(self.slug_url_kwarg)
        print(self.get_slug_field)
        print(self.slug_url_kwarg)
        print(self.get_object().slug)
        print("++++++++++++++++++")
        instance = form.save(commit=False)
        instance.question = Question.objects.get(slug=self.get_object().slug)
        instance.save()
        return HttpResponseRedirect(
            reverse("collab_app:question-detail", args=[self.get_object().slug])
        )


class QuestionCreate(CreateView):
    model = Question
    fields = ["question_title", "question_body"]
    template_name = "collab_app/add_question.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse("collab_app:question-list"))


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "collab_app/add_question.html"

    def get_success_url(self):
        return reverse("collab_app:question-list")


class QuestionDeleteView(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse("collab_app:question-list")


#   def add_question(request):
#     if request.method == "POST":
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("collab_app:question-list")
#     if request.method == "GET":
#         form = QuestionForm()
#     return render(request, "collab_app/add_question.html", {"form": form})


#     if kwargs != None:
#         return reverse_lazy('collab_app:question-detail', kwargs = {'pk': kwargs['']})


# class AnswerFormView(FormView):
#     form_class = AnswerForm
#     print(self)
#     success_url = reverse("collab_app:question-list")


# def question_detail_view(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     data = {"question": question}
#     if request.method == "POST":
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             ans = form.save(commit=False)
#             ans.question = question
#             ans.save()
#             return redirect("collab:question_list")
#         else:
#             data["form"] = form

#     else:
#         form = AnswerForm()
#         data["form"] = form
#     return render(request, "collab_app/question_detail.html", data)


# def add_answers(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == "POST":
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             ans = form.save(commit=False)
#             ans.question = question
#             ans.save()
#             redirect("/")

#         else:
#             for msg in form.error_messages:
#                 print(msg)
#                 # messages.error(request, f"{msg}: {form.error_messages[msg]}")

#     if request.method == "GET":
#         form = AnswerForm()
#     context = {"question": question, "form": form}
#     return render(request, "collab_app/add_answer.html", context)


# class AnswerForm(View):
#     question = get_object_or_404(Question, pk=question_id)

#     def get(self, request):
#         form = AnswerForm()

#     def post(self, request):
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             ans = form.save(commit=False)
#             ans.question = question
#             ans.save()
#             redirect("/")
#         else:
#             for msg in form.error_messages:
#                 print(msg)
#         context = {"question": question, "form": form}
#         return render(request, "collab_app/add_answer.html", context)

# def register(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"New account created: {username}")
#             login(request, user)
#             return redirect('collab_app:question-list')

#         else:
#             for msg in form.error_messages:
#                 messages.error(request, f"{msg}: {form.error_messages[msg]}")
#                 # print(form.error_messages[msg])
#             return render(request=request,
#                           template_name='collab_app/register.html',
#                           context={"form": form})

#     form = NewUserForm
#     return render(request=request,
#                   template_name="collab_app/register.html",
#                   context={"form": form})


# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully")
#     return redirect("collab_app:question-list")

# # def login_request(request):
# #     form = AuthenticationForm()
# #     return render(request = request,
# #                 template_name="collab_app/login.html",
# #                 context = {"form":form})


# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             # return redirect('collab_app:question-list')
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}")
#                 return redirect('/')
#             else:
#                 messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request=request,
#                   template_name='collab_app/login.html',
#                   context={"form": form})


# def get_env(request):
# return HttpResponse(str(os.environ.items()))
