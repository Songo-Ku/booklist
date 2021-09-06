from django import forms
from .models import Book


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title', 'language_book', 'published_date',
            'authors_name', 'isbn13_number', 'page_number', 'link_book_cover'
        )




