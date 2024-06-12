from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('create/<int:pk>', views.create, name='create'),
    path('result', views.result, name='result'),
    path('verify', views.verify, name='verify'),
    path('seal', views.seal, name='seal'),

]



