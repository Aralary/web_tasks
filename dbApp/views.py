from django.contrib import auth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, Http404, reverse
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import resolve
import datetime
import math
from .models import Profile, Answer, Question, Tag, t_questions, get_some_tags, get_best_members, get_good_questions, \
    get_new_questions
from .forms import LoginForm, SignupForm, QuestionForm, AnswerForm, SettingsForm


def pagination(request, pages, i: int):
    paginator = Paginator(pages, i)
    page = request.GET.get('page')
    pages = paginator.get_page(page)
    return pages


def index(request):
    request.session['continue'] = reverse('index')

    questions = Question.objects.all()
    questions = pagination(request, questions, 3)
    return render(request, "index.html",
                  {"questions": questions, "tags": get_some_tags(), "b_members": get_best_members(),
                   "page_name": "Questions"})


def hot(request):
    request.session['continue'] = reverse('hot')
    questions = get_good_questions()
    questions = pagination(request, questions, 3)
    return render(request, "index.html",
                  {"questions": questions, "tags": get_some_tags(), "b_members": get_best_members(),
                   "page_name": "Hot questions"})


def new(request):
    request.session['continue'] = reverse('new')
    questions = get_new_questions()
    questions = pagination(request, questions, 3)
    return render(request, "index.html",
                  {"questions": questions, "tags": get_some_tags(), "b_members": get_best_members(),
                   "page_name": "New questions"})


def signup(request):
    if request.method == "GET":
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
        p1 = request.POST['password']
        p2 = request.POST['repeat_password']
        print(p1)
        if p1 != p2:
            form.add_error(None, 'Passwords are not the same')
        else:
            print(p1)
            user = User.objects.create(
                username=request.POST['login'],
                first_name=request.POST['first_name'],
                email=request.POST['email'],
            )
            user.set_password(p1)
            print(user.username)
            print(user.password)
            if not Profile.objects.filter(user=user):
                profile = Profile.objects.create(
                    user=user,
                    img=request.POST['avatar']
                )
                profile.user.save()
                profile.save()
                return redirect(reverse('login'))
            else:
                form.add_error(None, 'Profile with this login is already exist')
    return render(request, "signup.html", {"tags": get_some_tags(), "b_members": get_best_members(), "form": form})


@login_required
def settings(request):
    if request.method == "GET":
        form = SettingsForm()
    else:
        form = SignupForm(data=request.POST)
        p1 = request.POST['password']
        p2 = request.POST['repeat_password']
        if p1 != p2:
            form.add_error(None, 'Passwords are not the same')
        else:
            profile = Profile.objects.get(user=request.user)
            profile.img = request.POST['avatar']
            profile.user.email = request.POST['email']
            profile.user.first_name = request.POST['first_name']
            profile.user.set_password(str(p1))
            profile.user.save()
            profile.save()
            auth.login(request, profile.user)
            next = request.session.pop('continue', reverse('settings'))
            return redirect(next)
    return render(request, "settings.html", {"tags": get_some_tags(), "b_members": get_best_members(), "form": form})


@login_required
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
                next = request.session.pop('continue', reverse('new'))
                return redirect(next)
            else:
                form.add_error(None, 'This question is already exist')
        else:
            form.add_error(None, 'Incorrect data')
    return render(request, "ask.html", {"tags": get_some_tags(), "b_members": get_best_members(), 'form': form})


def question(request, ix: str):
    q = Question.objects.filter(name=ix)
    request.session['continue'] = reverse('question_page', args=[ix])
    answers = q[0].answers.all()
    tags = get_some_tags()
    last_page = math.ceil((len(answers) + 1) / 3)
    answers = pagination(request, answers, 3)
    b_members = get_best_members()
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
                return redirect(reverse('question_page', args=[ix]) + '?page=%s' % str(last_page))
            else:
                form.add_error(None, 'Incorrect data')
        else:
            form.add_error(None, 'You must be authorized to answer the question')

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
    request.session['continue'] = reverse('tag_questions', args=[ix])
    tag_questions = t_questions(ix)
    tag_questions = pagination(request, tag_questions, 3)
    return render(request, "tag_questions.html",
                  {"tags": get_some_tags(), "tag": ix, "questions": tag_questions, "b_members": get_best_members()})


def logout(request):
    next = request.session.pop('continue', 'xxx')
    auth.logout(request)
    return redirect(next)
