from django.shortcuts import render, redirect
from .forms import BookForm

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books-list')  # Redirect to the list view
    else:
        form = BookForm()

    return render(request, 'create_book.html', {'form': form})


def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authors-list')  # Redirect to the list view for authors
    else:
        form = AuthorForm()

    return render(request, 'create_author.html', {'form': form})

    #balls
    