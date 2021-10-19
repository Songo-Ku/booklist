import django_filters
# import django_filters.orderingfilter
from .models import Book
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class BooklistFilter(django_filters.FilterSet):
    # paginate_by = 5
    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    )
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    def filter_by_order(self, queryset, name, value):
        expression = 'published_date' if value == 'ascending' else '-published_date'
        return queryset.order_by(expression)

    class Meta:
        model = Book
        # fields = ('title', 'authors_name', 'language_book', )
        fields = {
            'title': ['icontains'],
            'authors_name': ['icontains'],
            'language_book': ['icontains'],
            'published_date': ['gte', 'lte'],
        }

        # widgets = {
        #     'published_date': DateInput(),
        # }


class AvailFilter(django_filters.FilterSet):

    class Meta:
        model = Book
        widgets = {'published_date': DateInput(), }
        fields = ['published_date', 'title', 'authors_name', 'language_book', ]




