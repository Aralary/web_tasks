import random
from random import choice
from itertools import islice
from django.core.management.base import BaseCommand
from dbApp.models import Profile, Tag, Question, Answer
from django.contrib.auth.models import User
from faker import Faker
import glob
from random import shuffle, seed
from faker.providers.person.en import Provider


def fill_questions(n):
    users = Profile.objects.all()
    tags = Tag.objects.all()
    file_path_type = "static/*.jpg"
    images = glob.glob(file_path_type)
    for i in range(n):
        question = Question.objects.create(
            author=choice(users),
            name=Faker().sentence()[:200],
            text=". ".join(
                Faker().sentences(
                    Faker().random_int(min=2, max=5)
                )
            ),
            likes=random.randint(0, 1000),
            dislikes=random.randint(0, 1000),
            img=choice(images),
            date=Faker().date_between("-100d", "today")
        )
        for j in range(random.randint(5, 15)):
            answer = Answer.objects.create(
                text=". ".join(Faker().sentences(Faker().random_int(min=2, max=5))),
                likes=random.randint(0, 1000),
                dislikes=random.randint(0, 1000),
                author=choice(users),
                img=choice(images)
            )
            question.answers.add(answer)
        question.tags.add(choice(tags))
        question.tags.add(choice(tags))
        question.tags.add(choice(tags))


def fill_users(n):
    usernames = set()
    file_path_type = "static/*.jpg"
    images = glob.glob(file_path_type)

    while len(usernames) != n:
        usernames.add(Faker().user_name() + "№" + str(Faker().random.randint(0, 1000000)))

    for name in usernames:
        user = User.objects.create(
            username=name,
            password=Faker().password(),
            email=Faker().email()
        )
        Profile.objects.create(
            user=user,
            img=choice(images)
        )


def fill_tags(n):
    first_names = list(set(Provider.first_names))
    seed(4321)
    shuffle(first_names)

    for i in range(n):
        Tag.objects.create(name=Faker().word() + "№" + str(Faker().random.randint(0, 100000)))


def fill_db(n1, n2, n3):
    fill_users(n1)
    fill_tags(n2)
    fill_questions(n3)
