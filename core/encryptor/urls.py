from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('encryptor/', views.encryptor, name = 'encryptor'),
    path('decryptor/', views.decryptor, name = 'decryptor')
]

