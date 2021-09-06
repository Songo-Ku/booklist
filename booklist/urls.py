from django.urls import path, include

from . import views

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
]