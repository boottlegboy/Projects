from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100)
    year_published = models.PositiveIntegerField()
    copies_sold = models.PositiveIntegerField()

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField()
    publisher = models.CharField(max_length=100)