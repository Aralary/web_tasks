from django.contrib import auth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, Http404, reverse
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import resolve
import datetime

from .models import Profile, Answer, Question, Tag, t_questions, get_some_tags, get_best_members, get_good_questions, \
    get_new_questions
from .forms import LoginForm, SignupForm, QuestionForm, AnswerForm


def pagination(request, pages, i: int):
    paginator = Paginator(pages, i)
    page = request.GET.get('page')
    pages = paginator.get_page(page)
    return pages


def index(request):
    request.session['continue'] = reverse('index')
    questions = Question.objects.all()
    tags = get_some_tags()
    questions = pagination(request, questions, 3)
    b_members = get_best_members()
    return render(request, "index.html",
                  {"questions": questions, "tags": tags, "b_members": b_members, "page_name": "Questions"})


def hot(request):
    questions = get_good_questions()
    tags = get_some_tags()
    questions = pagination(request, questions, 3)
    b_members = get_best_members()
    return render(request, "index.html",
                  {"questions": questions, "tags": tags, "b_members": b_members, "page_name": "Hot questions"})


def new(request):
    questions = get_new_questions()
    tags = get_some_tags()
    questions = pagination(request, questions, 3)
    b_members = get_best_members()
    return render(request, "index.html",
                  {"questions": questions, "tags": tags, "b_members": b_members, "page_name": "New questions"})


def signup(request):
    if request.method == "GET":
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
    tags = get_some_tags()
    b_members = get_best_members()
    return render(request, "signup.html", {"tags": tags, "b_members": b_members, "form": form})


def settings(request):
    tags = get_some_tags()
    b_members = get_best_members()
    return render(request, "settings.html", {"tags": tags, "b_members": b_members})


def ask(request):
    if request.method == "GET":
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data['name']
            qs = Question.objects.filter(name=title)
            if not qs:
                q = Question.objects.create(
                    name=title,
                    text=form.cleaned_data['text'],
                    author=request.user.profile,
                    likes=0,
                    dislikes=0,
                    date=datetime.datetime.now(),
                    img="static/" + str(request.user.profile.img)
                )
                q.tags.set(form.cleaned_data['tags'])
                q.save()
                return redirect(reverse('new'))
            else:
                form.add_error(None, 'This question is already exist')
        else:
            form.add_error(None, 'Incorrect data')
    return render(request, "ask.html", {"tags": get_some_tags(), "b_members": get_best_members(), 'form': form})


def question(request, ix: str):
    q = Question.objects.filter(name=ix)

    if request.method == "GET":
        form = AnswerForm()

    else:
        form = AnswerForm(data=request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                ans = Answer.objects.create(
                    text=form.cleaned_data['text'],
                    author=request.user.profile,
                    likes=0,
                    dislikes=0,
                    img="static/" + str(request.user.profile.img)
                )
                q[0].answers.add(ans)
                form = AnswerForm()
            else:
                form.add_error(None, 'Incorrect data')
        else:
            form.add_error(None, 'You must be authorized to answer the question')

    answers = q[0].answers.all()
    tags = get_some_tags()
    answers = pagination(request, answers, 3)
    b_members = get_best_members()
    return render(request, "question.html",
                  {"question": q[0], "answers": answers, "tags": tags, "b_members": b_members, 'form': form})


def login(request):
    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        # print(user_form)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            # print(user)
            if user is not None:
                auth.login(request, user)
                next = request.session.pop('continue', 'index')
                return redirect(next)
            else:
                form.add_error(None, 'Incorrect login or password')
    return render(request, "login.html",
                  {"tags": get_some_tags(), "b_members": get_best_members(), "form": form})


def tag_questions(request, ix: str):
    tag_questions = t_questions(ix)
    tags = get_some_tags()
    tag_questions = pagination(request, tag_questions, 3)
    b_members = get_best_members()
    return render(request, "tag_questions.html",
                  {"tags": tags, "tag": ix, "questions": tag_questions, "b_members": b_members})


def logout(request):
    next = request.session.pop('continue', resolve(request.path_info).url_name)
    auth.logout(request)
    return redirect(next)
