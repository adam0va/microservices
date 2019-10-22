from django.urls import path
from authors_app import views

urlpatterns = [
    path('authors/', views.authors_list),
]
