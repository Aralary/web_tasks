from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f"This is text for question {i}",
        "tag1": f"tag {i + 1}",
        "tag2": f"tag {i - 1}",
        "tag3": f"tag {i * i}",
        "id": i
    } for i in range(0, 10)
]

ANSWERS = [
    {
        "title": f"Answer {i}"
    } for i in range(0, 10)
]

LOOK_QUESTIONS = [
    {
        "title": f"Question A{i}",
        "text": f"Text for question with number {i}",
        "tag1": f"tag {i + 1}",
        "tag2": f"tag {i - 1}",
        "tag3": f"tag {i * i}"
    } for i in range(1, 2)
]


def index(request):
    question_list = QUESTIONS
    paginator = Paginator(question_list, 3)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, "index.html", {"questions": questions})


def signup(request):
    return render(request, "signup.html")


def ask(request):
    return render(request, "ask.html")


def question(request, ix: int):
    answer_list = ANSWERS
    paginator = Paginator(answer_list, 2)

    page = request.GET.get('page')
    answers = paginator.get_page(page)
    return render(request, "question.html", {"question": QUESTIONS[ix], "answers": answers})


def login(request):
    return render(request, "login.html")