from django.urls import path
from . import views
urlpatterns=[
	path('',views.home,name='home'),
	path('login',views.login,name='login'),
	path('registration',views.registration,name='registration'),
	path('logout',views.logout,name='logout'),
	path('search',views.search,name='search'),
	path('upload',views.upload,name='upload'),
	path('profile',views.profile,name='profile'),
	path('settings',views.settings,name='settings'),
	path('single_search_person',views.single_search_person,name='single_search_person'),
	path('entire_search_person',views.entire_search_person,name='entire_search_person'),
	path('single_upload',views.single_upload,name='single_upload'),
	path('entire_upload',views.entire_upload,name='entire_upload'),
	path('todo_list',views.todo_list,name='todo_list'),
	path('check_progress',views.check_progress,name='check_progress'),
	path('partners',views.partners,name='partners')
]