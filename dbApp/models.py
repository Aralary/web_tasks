import resource

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    img = models.ImageField()

    def __str__(self):
        return f"{self.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class Answer(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(Profile, models.PROTECT)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    img = models.ImageField()


class Question(models.Model):
    name = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    author = models.ForeignKey(Profile, models.PROTECT)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    answers = models.ManyToManyField(Answer)
    img = models.ImageField()

    def __str__(self):
        return f"{self.name}"


def t_questions(_tag: str):
    questions = Question.objects.all()
    return [que for que in questions if [tag for tag in que.tags.all() if tag.name == _tag]]


def get_some_tags():
    questions = Question.objects.all()
    q = [que for que in questions if que.likes > 900]
    return q[0].tags.all()


def get_best_members():
    answers = Answer.objects.all()
    temp_res = [ans for ans in answers if ans.likes > 900]
    res = set()
    for i in range(5):
        res.add(temp_res[i].author)
    return res


def get_good_questions():
    questions = Question.objects.all()
    q = [que for que in questions if que.likes > 900]
    return q

class QuestionInstance(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
