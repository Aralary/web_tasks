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


class Command(BaseCommand):
    help = "filling db with random data"

    def add_arguments(self, parcer):
        parcer.add_argument("-u", "--users", type=int)
        parcer.add_argument("-t", "--tags", type=int)
        parcer.add_argument("-q", "--questions", type=int)
        parcer.add_argument("-a", "--answers", type=int)
        parcer.add_argument("-all", "--all", type=int)

    def handle(self, *args, **options):
        users_amount = options["users"]
        questions_amount = options["questions"]
        tags_amount = options["tags"]
        total_amount = options["all"]

        if total_amount:
            self.fill_tags(total_amount * 10)
            self.fill_users(total_amount * 10)
            self.fill_questions(total_amount * 100)
        else:
            if tags_amount:
                self.fill_tags(tags_amount * 10)
            if users_amount:
                self.fill_users(users_amount * 10)
            if questions_amount:
                self.fill_questions(questions_amount * 100)


    def fill_questions(self, n):
        users = list(Profile.objects.values_list('id', flat=True))
        tags = list(Tag.objects.values_list('name', flat=True))
        file_path_type = "static/*.jpg"
        images = glob.glob(file_path_type)
        for i in range(n):
            Answers = []
            for j in range(random.randint(5, 15)):
                answer = Answer(
                    text=". ".join(Faker().sentences(Faker().random_int(min=2, max=5))),
                    likes=random.randint(0, 1000),
                    dislikes=random.randint(0, 1000),
                    author=choice(users),
                    img=choice(images)
                )
                Answers.append(answer)
            question = Question.objects.create(
                author=choice(users),
                name=Faker().sentence()[:200],
                text=". ".join(
                    Faker().sentences(
                        Faker().random_int(min=2, max=5)
                    )
                ),
                answers=Answers,
                likes=random.randint(0, 1000),
                dislikes=random.randint(0, 1000),
                img=choice(images)
            )
            question.tags.add(choice(tags))

    # def fill_answers(self, n):
    #     print("filling ", n, " answers")
    #
    #     questions = list(Question.objects.values_list("id", flat=True))
    #     users = list(Profile.objects.values_list("id", flat=True))
    #     answers = []
    #
    #     for i in range(n):
    #         answer = Answer(
    #             fk_question_id=choice(questions),
    #             fk_profile_id=choice(users),
    #             text=". ".join(Faker().sentences(Faker().random_int(min=2, max=5))),
    #         )
    #         if Faker().random_int(min=0, max=5) == 0:
    #             answer.marked_correct = True
    #         answers.append(answer)
    #
    #     batch_size = 100
    #     n_batches = len(answers) // batch_size
    #     if len(answers) % batch_size != 0:
    #         n_batches += 1
    #     for i in range(n_batches):
    #         start = batch_size * i
    #         end = batch_size * (i + 1)
    #         Answer.objects.bulk_create(answers[start:end], batch_size)

    def fill_users(self, n):
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

    def fill_tags(self, n):
        first_names = list(set(Provider.first_names))
        seed(4321)
        shuffle(first_names)

        for i in range(n):
            Tag.objects.create(name=Faker().word() + "№" + str(Faker().random.randint(0, 100000)))
