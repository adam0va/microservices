from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import TemplateView
from gateway_app import views


urlpatterns = [
	path('', TemplateView.as_view(template_name="gateway/main.html"), name='gateway_main'),
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

