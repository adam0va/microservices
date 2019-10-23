from django.conf.urls import url
from authors_app import views

urlpatterns = [
    url(r'^authors/$', views.AuthorList.as_view()),
    url(r'^authors/(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$', 
    	views.AuthorDetail.as_view()),
]
