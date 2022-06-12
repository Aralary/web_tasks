import string

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from .models import Profile, Answer, Question, Tag, t_questions, get_some_tags, get_best_members, get_good_questions


def pagination(request, pages, i: int):
    paginator = Paginator(pages, 3)
    page = request.GET.get('page')
    pages = paginator.get_page(page)
    return pages


def index(request):
    questions = Question.objects.all()
    tags = get_some_tags()
    questions = pagination(request, questions, 3)
    b_members = get_best_members()
    return render(request, "index.html", {"questions": questions, "tags": tags, "b_members": b_members, "page_name": "Questions"})


def hot(request):
    questions = get_good_questions()
    tags = get_some_tags()
    questions = pagination(request, questions, 3)
    b_members = get_best_members()
    return render(request, "index.html", {"questions": questions, "tags": tags, "b_members": b_members, "page_name": "Hot questions"})


def signup(request):
    tags = get_some_tags()
    b_members = get_best_members()
    return render(request, "signup.html", {"tags": tags, "b_members": b_members})


def settings(request):
    tags = get_some_tags()
    b_members = get_best_members()
    return render(request, "settings.html", {"tags": tags, "b_members": b_members})


def ask(request):
    tags = get_some_tags()
    b_members = get_best_members()
    return render(request, "ask.html", {"tags": tags, "b_members": b_members})


def question(request, ix: str):
    q = Question.objects.filter(name=ix)
    answers = q[0].answers.all()
    tags = get_some_tags()
    answers = pagination(request, answers, 3)
    b_members = get_best_members()
    return render(request, "question.html",
                  {"question": q[0], "answers": answers, "tags": tags, "b_members": b_members})


def login(request):
    tags = get_some_tags()
    b_members = get_best_members()
    return render(request, "login.html", {"tags": tags, "b_members": b_members})


def tag_questions(request, ix: str):
    tag_questions = t_questions(ix)
    tags = get_some_tags()
    tag_questions = pagination(request, tag_questions, 3)
    b_members = get_best_members()
    return render(request, "tag_questions.html",
                  {"tags": tags, "tag": ix, "questions": tag_questions, "b_members": b_members})
