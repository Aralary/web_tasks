from django.db import models


class Author(models.Model):
    nickname = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.nickname}"


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class Answer(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(Author, models.PROTECT)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    img = models.ImageField()


class Question(models.Model):
    name = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    author = models.ForeignKey(Author, models.PROTECT)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    answers = models.ManyToManyField(Answer)
    img = models.ImageField()

    def __str__(self):
        return f"{self.name}"



class QuestionInstance(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
