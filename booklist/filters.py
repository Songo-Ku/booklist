import django_filters
# import django_filters.orderingfilter
from .models import Book


class BooklistFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    )
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Book
        # fields = ('title', 'authors_name', 'language_book', )
        fields = {
            'title': ['icontains'],
            'authors_name': ['icontains'],
            'language_book': ['icontains'],
            'created': ['gte', 'lte'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'ascending' else '-created'
        return queryset.order_by(expression)


