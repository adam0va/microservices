from django.urls import path
from books_app import views

urlpatterns = [
    path('books/', views.books_list),
]