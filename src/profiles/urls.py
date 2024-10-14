from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('<str:username>/', views.detail_view, name='profile')
]