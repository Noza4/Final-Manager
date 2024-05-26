from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import date, timedelta
from django.db.models import F


class Genre(models.Model):
    genre = models.CharField(max_length=100, null=False, verbose_name="Genre")

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Author(models.Model):
    author = models.CharField(max_length=100, null=True, verbose_name="Author")

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class ValidationError(Exception):
    pass


class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name="Title")
    author = models.ManyToManyField(Author, verbose_name="Author")
    genre = models.ManyToManyField(Genre, verbose_name="Genre")
    publication_date = models.DateField(verbose_name="Publication Date")
    stock = models.PositiveIntegerField(verbose_name="Stock")
    popularity = models.PositiveIntegerField(default=0)
    image = models.ImageField(default='cover.jpg')

    def clean(self):
        if self.publication_date > date.today():
            raise ValidationError("Publication date cannot be in the future.")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class CustomUser(AbstractUser):
    full_name = models.CharField('full name', max_length=120)
    email = models.EmailField('email address', unique=True)
    personal_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r'^\d{13}$', 'Personal number must be 13 digits.')]
    )
    birth_date = models.DateField(null=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'birth_date']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_user = True
        super().save(args, **kwargs)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        blank=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class BookReservation(models.Model):
    choice = [
        ("Reserved", "Reserved"),
        ("On Loan", "On Loan"),
        ("Cancelled", "Cancelled"),
        ("Returned", "Returned"),
        ("Late", "Late")
    ]

    name = models.CharField(max_length=150)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    email = models.EmailField()
    reserve_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(choices=choice, max_length=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.return_date = self.reserve_date + timedelta(days=7)
            self.book.stock = F('stock') - 1
            self.book.popularity = F('popularity') + 1
            self.book.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Book Reservation"
