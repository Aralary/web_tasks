import string

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from .models import Author, Answer, Question, Tag


def index(request):
    questions = Question.objects.all()
    tags = Tag.objects.all()

    paginator = Paginator(questions, 3)
    page = request.GET.get('page')
    questions = paginator.get_page(page)

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
    # answers = q_answers.objects.all()
    tags = Tag.objects.all()

    paginator = Paginator(answers, 3)
    page = request.GET.get('page')
    answers = paginator.get_page(page)

    return render(request, "question.html", {"question": q[0], "answers": answers, "tags": tags})


def login(request):
    tags = Tag.objects.all()
    return render(request, "login.html",  {"tags": tags})


def tag_questions(request, ix: str):
    questions = Question.objects.all()
    tag_questions = [que for que in questions if [tag for tag in que.tags.all() if tag.name == ix]]

    tags = Tag.objects.all()
    paginator = Paginator(tag_questions, 3)

    page = request.GET.get('page')
    tag_questions = paginator.get_page(page)
    return render(request, "tag_questions.html", {"tags": tags, "tag": ix, "questions": tag_questions})


