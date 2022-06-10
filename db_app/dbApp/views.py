import string

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from .models import Author, Answer, Question, Tag, t_questions


def pagination(request, pages, i: int):
    paginator = Paginator(pages, 3)
    page = request.GET.get('page')
    pages = paginator.get_page(page)
    return pages


def index(request):
    questions = Question.objects.all()
    tags = Tag.objects.all()
    questions = pagination(request, questions, 3)
    return render(request, "index.html", {"questions": questions, "tags": tags})


def signup(request):
    tags = Tag.objects.all()
    return render(request, "signup.html", {"tags": tags})


def settings(request):
    tags = Tag.objects.all()
    return render(request, "settings.html", {"tags": tags})


def ask(request):
    tags = Tag.objects.all()
    return render(request, "ask.html", {"tags": tags})


def question(request, ix: str):
    q = Question.objects.filter(name=ix)
    answers = q[0].answers.all()
    tags = Tag.objects.all()
    answers = pagination(request, answers, 3)
    return render(request, "question.html", {"question": q[0], "answers": answers, "tags": tags})


def login(request):
    tags = Tag.objects.all()
    return render(request, "login.html",  {"tags": tags})


def tag_questions(request, ix: str):
    questions = Question.objects.all()
    tag_questions = t_questions(ix)
    tags = Tag.objects.all()
    tag_questions = pagination(request, tag_questions, 3)
    return render(request, "tag_questions.html", {"tags": tags, "tag": ix, "questions": tag_questions})


