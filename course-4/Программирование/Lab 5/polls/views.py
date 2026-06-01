from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PollCreateForm, RegisterForm
from .models import Question, Choice


def index_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("polls:index")


def index(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.all()
    return render(request, "polls/index.html", {"questions": questions})


def detail(request: HttpRequest, pk: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=pk)
    return render(request, "polls/detail.html", {"question": question})


def results(request: HttpRequest, pk: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=pk)
    return render(request, "polls/results.html", {"question": question})


@login_required
def vote(request: HttpRequest, pk: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=pk)
    try:
        choice_id = int(request.POST["choice"])
        selected_choice = question.choices.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist, ValueError):
        messages.error(request, "Вы не выбрали вариант ответа.")
        return render(
            request,
            "polls/detail.html",
            {"question": question},
        )
    selected_choice.votes += 1
    selected_choice.save()
    return redirect("polls:results", pk=question.pk)


@login_required
def poll_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PollCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            choices_lines = form.cleaned_data["choices"]
            question = Question.objects.create(
                question_text=title,
                author=request.user,
            )
            for text in choices_lines:
                Choice.objects.create(question=question, choice_text=text)
            messages.success(request, "Опрос успешно создан.")
            return redirect("polls:detail", pk=question.pk)
    else:
        form = PollCreateForm()
    return render(request, "polls/poll_form.html", {"form": form})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("polls:index")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Простой logout по GET-запросу с редиректом на страницу логина.
    """
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("login")
