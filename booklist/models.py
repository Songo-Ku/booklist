from django.db import models
from django.utils import timezone
# from django.conf import settings
from django.urls import reverse
import datetime


class Book(models.Model):
    # added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    language_book = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True, help_text="example: 2017-03-14")
    published_date = models.CharField(max_length=40, default='unknown', help_text="example: 2017-03-14")
    isbn13_number = models.IntegerField()
    authors_name = models.CharField(default='unknown', max_length=300)
    page_number = models.IntegerField(default=0)
    link_book_cover = models.URLField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.published_date}'

    def was_published_recently(self):
        return self.published_date >= timezone.now() - datetime.timedelta(days=30)

    def get_absolute_url(self):
        return reverse("booklist:book_detail", kwargs={"id": self.id})









