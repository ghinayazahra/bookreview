from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.signin, name='login'),
    path('books', views.showbooks, name='books'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('book/<int:book_id>', views.book, name='book')

]