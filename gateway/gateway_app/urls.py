from django.conf.urls import url
from gateway_app import views


urlpatterns = [
    url(r'^readers/$', views.AllReadersView.as_view()),
    url(r'^readers/(?P<reader_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ReaderView.as_view()),
    url(r'^authors/$', views.AllAuthorsView.as_view()),
    url(r'^authors/(?P<author_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.AuthorView.as_view()),
    url(r'^books/$', views.AllBooksView.as_view()),
    url(r'^books/(?P<book_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.BookView.as_view()),
]

