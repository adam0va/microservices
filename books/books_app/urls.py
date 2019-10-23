from django.conf.urls import url
from books_app import views

urlpatterns = [
    url(r'^books/$', views.BookList.as_view()),
    url(r'^books/(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$', 
    	views.BookDetail.as_view()),
]
