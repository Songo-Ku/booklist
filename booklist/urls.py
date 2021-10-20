from django.urls import path, include

from . import views
from django_filters.views import FilterView
from .models import Book

app_name = 'booklist'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('books_import_phrase/', views.books_import_phrase, name='books_import_phrase'),
    #  trzeba to zmienic i dac wszystko przez views book import view
    path('books_import/', views.BookImportView.as_view(), name='books_import'),
    path('book/<int:id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add_new_book/', views.BookCreateView.as_view(), name='book_add'),
    path('<int:id>/delete-book/', views.BookDeleteView.as_view(), name='book_delete'),
    path('<int:id>/update-book/', views.BookUpdateView.as_view(), name='book_update'),
    path('filter-search-ordering/', views.BookFilterSearchListView.as_view(), name='filter_search_order'),
    # path('filter_avail/', views.BooksFilterAvailFilter.as_view(), name='filter_avail'),
    # path('filter_avail/', views.BookFilterView.as_view(), name='filter_avail'),
    # path('filterset_filter/', views.BookListView.as_view(), name='filterset_filter'),
    # path('filterview/', FilterView.as_view(filterset_class=views.F), name='filterview'), # nie ma paginacji
    path('moj_filter_with_pag/', views.MojFilterWithPag.as_view(), name='moj_filter_with_pag'),  # ale to juz nie dziala
    path('bookfiltersearchpag/', views.BookFilterSearchPag.as_view(), name='bookfiltersearchpag'),

]
