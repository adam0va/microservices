from django.conf.urls import url
from readers_app import views

urlpatterns = [
    url(r'^readers/$', views.ReaderList.as_view()),
    url(r'^readers/(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$', 
    	views.ReaderDetail.as_view()),
]
