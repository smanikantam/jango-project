from django.urls import path
from . import views
urlpatterns=[
	path('',views.index,name='index'),
	path('login',views.login,name='login'),
	path('registration',views.registration,name='registration'),
	path('add',views.add,name='add'),
	path('logout',views.logout,name='logout'),
	path('retrieve',views.retrieve,name='retrieve'),
	path('single_upload',views.single_upload,name='single_upload'),
	path('search',views.search,name='search')

]