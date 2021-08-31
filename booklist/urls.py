from django.urls import path, include

from . import views

app_name = 'bestbooks'
urlpatterns = [



    # path('', views.IndexView.as_view(), name='index'),
    # path('main/', views.mainview, name='main'),
    # path('<int:pk>/', views.detailview, name='detail'),
    # # path('<int:pk>/book/', views.Detail_Book_View.as_view(), name='book_detail'),
    #
    # path('<int:pk>/book/', views.detail_book_view, name='book_detail'),
    #
    # path('book/new/', views.book_new, name='book_new'),
    # path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),

    # path('<int:pk>/book/comment/add', views.add_comment_view, name='add_comment'),
    # path('<int:pk>/book/comment/edit', views.edit_comment_view, name='edit_comment'),

    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('authors/', views.authors_list, name='authors_list'),

]