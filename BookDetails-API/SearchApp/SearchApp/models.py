from django.db import models
from pymongo import db

userCollections = db['authors']

class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    class Meta:
        app_label = 'SearchApp'