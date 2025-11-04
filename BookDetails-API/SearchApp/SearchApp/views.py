from django.http import JsonResponse
from .models import Book 
from .models import userCollections
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_book_details(request, isbn):
    try:
        book = Book.objects.get(isbn=isbn)
        data = {
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            
        }
        return JsonResponse(data)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)