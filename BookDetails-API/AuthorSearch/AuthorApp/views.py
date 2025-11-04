from django.shortcuts import render
from .models import userCollections
from .models import Author, Book
from rest_framework.decorators import api_view
from rest_framework.response import Response

def search_author(request):
    if request.method == "POST":
        author_name = request.POST.get('author_name')
        authors = Author.objects.filter(name__icontains=author_name)
        return render(request, 'books/author_list.html', {'authors': authors})
    return render(request, 'books/search_author.html')

def books_by_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author)
    return render(request, 'books/books_by_author.html', {'author': author, 'books': books})