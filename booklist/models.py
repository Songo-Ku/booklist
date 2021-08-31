from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Author(models.Model):
    first_name = models.CharField (max_length=200)
    last_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    language_book = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField('published date')
    isbn_number = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(13)])
    # validate integers i dont know how to connect it with isbn number
    # link from take it https://docs.djangoproject.com/en/2.2/ref/validators/
    # MaxLengthValidator i MinLengthValidator
    page_number = models.IntegerField(default=0)
    link_book_cover = models.URLField(null=True, blank=True)
    author = models.ForeignKey('booklist.Author', on_delete=models.CASCADE, related_name='books')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.published_date >= timezone.now() - datetime.timedelta(days=30)


class AuthorDescription(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='personals')
    # birthday = models.DateField(null=True, blank=True)
    # death_day = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name {self.author.first_name} last name {self.author.last_name} '

    def calculate_age(self):
        import datetime
        if self.death_day:
            return int((self.death_day - self.birthday).days / 365.25)
        # print(int((datetime.date.today() - self.birthday).days / 365.25))
        return int((datetime.date.today() - self.birthday).days / 365.25)

    def is_alive(self):
        if self.death_day:
            return False
        return True

# I am not sure it is correctly but it works.
    age = property(calculate_age)







