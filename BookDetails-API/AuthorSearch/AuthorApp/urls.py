from django.urls import path
from . import views

urlpatterns = [
    path('search_author/', views.search_author, name='search_author'),
    path('books_by_author/<int:author_id>/', views.books_by_author, name='books_by_author'),
]