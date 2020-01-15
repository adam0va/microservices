from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from gateway_app import views


urlpatterns = [

    url(r'^token-auth/$', views.AuthView.as_view()),

    url(r'^readers/$', views.AllReadersView.as_view()),
    url(r'^readers/(?P<reader_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ReaderView.as_view()),

    url(r'^authors/$', views.AllAuthorsView.as_view()),
    url(r'^authors/(?P<author_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.AuthorView.as_view()),

    url(r'^books/$', views.AllBooksView.as_view()),
    url(r'^books/(?P<book_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.BookView.as_view()),

    url(r'^ologin/$', views.OLoginView.as_view()),
    url(r'^api/o/redirect/$', views.ORedirectView.as_view()),
]

