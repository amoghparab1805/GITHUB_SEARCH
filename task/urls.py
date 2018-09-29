from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
app_name = 'task'
urlpatterns = [
	path('login/', auth_views.login, name='login'),
	path('logout/', auth_views.logout, name='logout'),
	url(r'^home/$', TemplateView.as_view(template_name='task/home.html'), name='home'),
	url(r'^create/$', views.create, name='create'),
	url(r'^search/$', views.usersearch, name='usersearch'),
	url(r'^commits/(?P<repo_name>\w.+)/$', views.usercommit, name='usercommit'),
]