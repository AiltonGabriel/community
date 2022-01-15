from django.urls import path

from . import views

app_name = 'apis'
urlpatterns = [
    path('search', views.search, name='search'),
    path('search/<slug:type>', views.search_type, name='search_type'),

    path('topic/<slug:item_type>/<int:topic_id>', views.topic, name='topic'),
    path('topic/create/<slug:parent_item_type>/<slug:id_parent_item>', views.create_topic, name='create_topic'),

    #---------------------------------------------------------------------------
    # Movies - Api The Movie Database(TMDB)
    path('search/movies/genre', views.search_movies_genre, name='search_movies_genre'),
    path('details/movies/<int:movie_id>', views.details_movie, name='details_movie'),

    #---------------------------------------------------------------------------
    # TV - Api The Movie Database(TMDB)
    path('search/tv/genre', views.search_tv_genre, name='search_tv_genre'),
    path('details/tv/<int:tv_id>', views.details_tv, name='details_tv'),

    #---------------------------------------------------------------------------
    # Books - Api Google Books
    path('search/books/genre', views.search_books_genre, name='search_books_genre'),
    path('search/books/author', views.search_books_author, name='search_books_author'),
    path('details/books/<slug:book_id>', views.details_book, name='details_book'),

]