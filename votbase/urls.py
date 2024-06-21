from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote', views.vote, name='vote'),
    path('create', views.create, name='create'),
    path('results', views.result, name='result'),
    path('register', views.register_view, name='register'),
    path('login', views.singing, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('candidate', views.candidate, name='candidate'),
    path('vote-list', views.vote_list, name='vote_list'),
    path('encrypted-info', views.show_encrypted_info, name='show_encrypted_info'),

]
