from django.urls import path
from . import views

urlpatterns = [
    path('create_book/', views.create_book, name='create_book'),
    path('create-author/', create_author, name='create-author'),
]
