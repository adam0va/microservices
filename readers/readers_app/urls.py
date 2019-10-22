from django.urls import path
from readers_app import views

urlpatterns = [
    path('readers/', views.readers_list),
]
