from . import views
# from django.conf.urls import url
# from django.contrib import admin
from django.urls import path, include

app_name = 'api-booklist'
urlpatterns = [
    path('', views.BookAPIView.as_view(), name='post-create'),
    path('<int:pk>/', views.BookRudView.as_view(), name='post-rud'),

]
