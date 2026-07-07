from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_us, name='about_us'),
]
