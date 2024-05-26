from random import randint
from django.core.management.base import BaseCommand
from faker import Faker
from manager.models import Author, Genre, Book
import random

class Command(BaseCommand):
    help = 'Generate random books'

    def handle(self, *args, **kwargs):
        faker = Faker()
        genres = ['Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy', 'Biography', 'Children', 'Romance']

        for genre in genres:
            Genre.objects.get_or_create(genre=genre)

        for _ in range(100):
            Author.objects.create(author=faker.name())

        genreobjs = list(Genre.objects.all())
        author_objs = list(Author.objects.all())

        for _ in range(1000):
            title = faker.sentence(nb_words=4)
            pub_date = faker.date_between(start_date='-50y', end_date='today')
            stock = randint(1, 20)
            genre = random.choice(genreobjs)
            book = Book.objects.create(title=title, publication_date=pub_date, stock=stock)
            author = random.choice(author_objs)
            book.author.add(author)
            book.genre.add(genre)

        self.stdout.write(self.style.SUCCESS('Successfully generated books'))
