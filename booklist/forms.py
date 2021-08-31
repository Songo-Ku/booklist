from django import forms
from .models import Author, Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'description', 'published_date', 'author')


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('author', 'comment_text')