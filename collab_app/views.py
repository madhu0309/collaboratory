import os
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormView, CreateView
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from collab_app.forms import QuestionForm, AnswerForm, CommentForm
from collab_app.models import Question, Comment, Answer
from users.models import CustomUser
from collab_app.serializers import UserSerializer

# CLASS BASED VIEWS


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
            question_list = Question.objects.filter(
                Q(question_title__icontains=query)  # | Q(author__icontains=query)
            )
        else:
            question_list = Question.objects.all()
        paginator = Paginator(question_list, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            no_of_pages = paginator.page(page)
        except PageNotAnInteger:
            no_of_pages = paginator.page(1)
        except EmptyPage:
            no_of_pages = paginator.page(paginator.num_pages)

        context["question_lists"] = no_of_pages
        if self.request.GET.get("q") != None:
            context["search"] = self.request.GET.get("q")
        return context


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


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["question_title", "question_body"]
    template_name = "collab_app/add_question.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return HttpResponseRedirect(reverse("collab_app:question-list"))


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "collab_app/add_question.html"

    def get_success_url(self):
        return reverse("collab_app:question-list")


class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy("collab_app:question-list")


# FUNCTION BASED VIEWS


def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("collab_app:question-list")
    if request.method == "GET":
        form = QuestionForm()
    return render(request, "collab_app/add_question.html", {"form": form})


def is_valid_queryparam(param):
    return param != "" and param is not None


def question_list_view(request):
    QUESTIONS_PER_PAGE = 2
    context = {}
    question_list = Question.objects.all()
    if request.is_ajax():
        queryset = Question.objects.filter(
            question_title__icontains=request.GET.get("search", None)
        )
        list = []
        for i in queryset:
            list.append(i.question_title)
        data = {
            "list": list,
        }
        print(data)
        return JsonResponse(data)
    print(request.GET)
    question_title_contains_query = request.GET.get("q", "")
    context["query"] = str(question_title_contains_query)
    # id_exact_query = request.GET.get()
    # question_title_or_body_query = request.GET.get()
    print(question_title_contains_query)
    if is_valid_queryparam(question_title_contains_query):
        question_list = question_list.filter(
            question_title__icontains=question_title_contains_query
        )
    # Search with sorted
    # quesion_list = sorted(question_title_contains_query())
    # Search Using Id
    # elif id_exact_query != "" and id_exact_query is not None:
    #     question_list = question_list.filter(id=id_exact_query)
    # Search by using two objects
    # elif question_title_or_body_query != '' and question_title_or_body is not None:
    #     question_list = question_list.filter(Q(question_title__icontains=question_title_or_body) |
    #                                          Q(question_title__icontains=question_title_or_body)).distinct()
    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(question_list, QUESTIONS_PER_PAGE)

    try:
        question_list = paginator.page(page)
    except PageNotAnInteger:
        question_list = paginator.page(QUESTIONS_PER_PAGE)
    except EmptyPage:
        question_list = paginator.page(paginator.num_pages)

    context["question_lists"] = question_list
    return render(request, "collab_app/question_list.html", context)


@login_required
def question_detail_view(request, question_id):
    instance = get_object_or_404(Question, pk=question_id)
    # data["comments"] = comments
    # data = {"question": question}
    # comments = Comment.objects.filter(question=question)
    # data["comments"] = comments
    # comment_message = request.POST.get("message", "")
    # print(comment_message)
    context = {}
    initial_data = {"content_type": instance.get_content_type, "object_id": instance.id}
    # import pdb;pdb.set_trace()
    comment_form_var = CommentForm()
    if request.method == "GET":
        answer_form_var = AnswerForm(request.GET or None)
        comment_form_var = CommentForm(request.GET or None, initial=initial_data)
    if request.method == "POST":
        answer_form_var = AnswerForm(request.POST or None)
        comment_form_var = CommentForm(request.POST or None, initial=initial_data)
        if "answer-form" in request.POST:
            if answer_form_var.is_valid():
                quest = answer_form_var.save(commit=False)
                quest.question = instance
                quest.save()
                return redirect("collab_app:question-list")
            else:
                context["answer_form"] = answer_form_var
                for msg in answer_form_var.error_messages:
                    print(msg)
                    messages.error(
                        request, f"{msg}: {answer_form_var.error_messages[msg]}"
                    )

        elif "comment-form" in request.POST:
            print(comment_form_var)
            if comment_form_var.is_valid():
                # form = form.save(commit=False)
                print(comment_form_var.cleaned_data)
                # import pdb;pdb.set_trace()
                c_type = comment_form_var.cleaned_data.get("content_type")
                content_type = ContentType.objects.get(
                    app_label=c_type.split()[0], model=c_type.split()[2]
                )
                obj_id = comment_form_var.cleaned_data.get("object_id")
                message = comment_form_var.cleaned_data.get("message")
                parent_obj = None
                try:
                    parent_id = int(request.POST.get("parent_id"))
                except:
                    parent_id = None

                if parent_id:
                    parent_qs = Comment.objects.filter(id=parent_id)
                    if parent_qs.exists() and parent_qs.count() == 1:
                        parent_obj = parent_qs.first()

                comm = comment_form_var.save(commit=False)
                comm.user = request.user
                comm.content_type = content_type
                comm.object_id = obj_id
                comm.message = message
                comm.parent = parent_obj
                comm.save()

                # new_comment, created = Comment.objects.get_or_create(
                #     user=request.user,
                #     content_type=content_type,
                #     object_id=obj_id,
                #     message=message,
                #     parent=parent_obj,
                # )
                # if created:
                #     print("Yeah created")
                return HttpResponseRedirect(
                    reverse("collab_app:question-detail", args=[instance.id])
                )
            else:
                print(comment_form_var.errors)
    comments = instance.comments
    context = {
        "instance": instance,
        "comments": comments,
        "comment_form": comment_form_var,
        "answer_form": answer_form_var,
    }
    return render(request, "collab_app/question_detail.html", context)

    #             return HttpResponseRedirect(
    #                 reverse("collab_app:question-detail", args=[question.id])
    #             )
    #         else:
    #             data["form"] = form
    #             # for msg in form.error_messages:
    #             #     print(msg)
    #             #     messages.error(request, f"{msg}: {form.error_messages[msg]}")

    #     # else:
    #     #     form = CommentForm
    #     #     data["form"] = form

    # # Comment.objects.create(user=user, message=comment_message, content_object=question)

    # return render(request, "collab_app/question_detail.html", data)


def delete_question(request, slug):
    context = {}
    question = Question.objects.all()
    context = question.objects.filter(slug=slug).delete()
    return render(request, context)


def add_comment_view(request):
    # comment = get_object_or_404(Question, pk=question_id)  # filter(question=question)
    comment = Comment.objects.all()
    data = {"comments": comment}

    if request.method == "POST":
        print(request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            comment_obj = form.save(commit=False)
            comment_id = request.POST.get("comment_id", "")
            if comment_id != None:
                comment_obj.parent_id = comment_id
                comment_obj.save()
            else:
                comment_obj.save()

        else:
            print(form.errors)
    else:
        form = CommentForm()
        data["form"] = form
    return render(request, "collab_app/thread.html", data)  # data)


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


def get_env(request):
    return HttpResponse(str(os.environ.items()))


# REST FRAMEWORK


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited 
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


def upvote(request,answer_id):
    print(answer_id)
    answer = Answer.objects.get(pk=answer_id)
    question_id = answer.question_id
    x = answer.votes.up(request.user.id)
    print(x)
    return HttpResponseRedirect(reverse("collab_app:question-detail", args=[question_id]))

def downvote(request,answer_id):
    print(answer_id)
    answer = Answer.objects.get(pk=answer_id)
    question_id = answer.question_id
    x = answer.votes.down(request.user.id)
    print(x)
    return HttpResponseRedirect(reverse("collab_app:question-detail", args=[question_id]))