from django.conf.urls import url
from auth_app import views

urlpatterns = [
    url(r'^user_info/$', views.GetUserInfoView.as_view()),
]