from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

from bukuku.models import Book, Author, Review, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    user = request.user.username if request.user.is_authenticated else None

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'user': user,
    }

    # Render the HTML templates index.html with the data in the context variable


    return render(request, 'bukuku/index.html', context=context)

def signin(request):
    if request.method == 'GET':
        return render(request, 'bukuku/login.html')
    else:
        username = request.POST['username']
        psw = request.POST['psw']

        user = authenticate(username=username, password=psw)
        if user is not None:
            login(request,user)
            books=Book.objects.order_by('id')[0:]
            user = request.user.username if request.user.is_authenticated else None
            return render(request, 'bukuku/books.html', {'books': books, 'user': user})
        else:
            return HttpResponse('Your ID is wrong!')

def signup(request):
    if request.method=='GET':
        return render(request, 'bukuku/signup.html')
    else:
        if not request.POST['password'] == request.POST['repeat_password']:
            return render(request, 'bukuku/signup.html')
        else:
            user = User.objects.create_user(request.POST['username'], None, request.POST['password'])
            user.username = request.POST['username']
            user.save()
            login(request, user)
            user = request.user.username if request.user.is_authenticated else None
            return render(request, 'bukuku/books.html', {'user':user})


def showbooks(request):
    user = request.user.username if request.user.is_authenticated else None
    books = Book.objects.all()
    return render(request, 'bukuku/books.html', {'books': books, 'user': user})

def signout(request):
    logout(request)
    return redirect('/bukuku')

def book(request, book_id):
    if request.method == 'GET':
        book = Book.objects.get(pk=book_id)
        user = request.user.username if request.user.is_authenticated else None
        return render(request, 'bukuku/book.html', {'book': book, 'user': user})
    else:
        book = Book.objects.get(pk=book_id)
        review = Review(book=book, review=request.POST['review'], writer=request.user)

        review.save()
        return render(request, 'bukuku/book.html', {'book': book, 'user': request.user.username})











