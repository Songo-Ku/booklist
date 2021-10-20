from django import forms
from .models import Book


class DateInput(forms.DateInput):
    input_type = 'date'


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title', 'language_book', 'published_date',
            'authors_name', 'isbn13_number', 'page_number', 'link_book_cover'
        )
        widgets = {
            'published_date': DateInput(),
        }


class BookFilterSearchPagForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'authors_name': ['icontains'],
            'language_book': ['icontains'],
            'published_date': ['gte', 'lte'],
        }
        widgets = {
            'published_date': DateInput(),
        }


class InputForm(forms.Form):
    title = forms.CharField(max_length=200)
    # last_name = forms.CharField(max_length=200)
    # roll_number = forms.IntegerField(
    #     help_text="Enter 6 digit roll number"
    # )
    published_date_gte = forms.CharField(widget=forms.DateInput())


