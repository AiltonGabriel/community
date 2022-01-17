import requests
from django.conf import settings

API_KEYS = {
    'tmdb': settings.TMDB_API_KEY,
    'google_books': settings.GOOGLE_BOOKS_API_KEY
}

FIREBASE_CREDENTIALS = """apiKey: \'{}\',
            authDomain: \"{}\",
            projectId: \"{}\",
            storageBucket: \"{}\",
            messagingSenderId: \"{}\",
            appId: \"{}\",
            measurementId: \"{}\"
        """.format(settings.FIREBASE_API_KEY, settings.FIREBASE_AUTH_DOMAIN, settings.FIREBASE_PROJECT_ID, settings.FIREBASE_STORAGE_BUCKET, settings.FIREBASE_MESSAGING_SENDER_ID, settings.FIREBASE_APP_ID, settings.FIREBASE_MEASUREMENT_ID)

#-----------------------------------------------------------------------------------------------------------------------
# Movies - Api The Movie Database(TMDB)
def request_movie(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR")
    return response
def request_all_genres_movies():
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR")
    return response
def request_search_movies(query, page=1):
    response = requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR&query=" + str(query) + "&page=" + str(page) + "&include_adult=true")
    return response
def request_search_movies_by_genre(genre_id, page=1):
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR&sort_by=popularity.desc&include_adult=true&page=" + str(page) + "&with_genres=" + str(genre_id))
    return response

#-----------------------------------------------------------------------------------------------------------------------
# TV - Api The Movie Database(TMDB)
def request_tv(tv_id):
    response = requests.get("https://api.themoviedb.org/3/tv/" + str(tv_id) + "?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR")
    return response
def request_all_genres_tv():
    response = requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR")
    return response
def request_search_tv(query, page=1):
    response = requests.get("https://api.themoviedb.org/3/search/tv?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR&query=" + str(query) + "&page=" + str(page) + "&include_adult=true")
    return response
def request_search_tv_by_genre(genre_id, page=1):
    response = requests.get("https://api.themoviedb.org/3/discover/tv?api_key=" + API_KEYS['tmdb'] + "&language=pt-BR&sort_by=popularity.desc&include_adult=true&page=" + str(page) + "&with_genres=" + str(genre_id))
    return response

#-----------------------------------------------------------------------------------------------------------------------
# Books - Api Google Books
def request_book(book_id):
    response = requests.get("https://www.googleapis.com/books/v1/volumes/" + book_id + "?key=" + API_KEYS['google_books'])
    return response
def request_search_book(query, page=1):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?key=" + API_KEYS['google_books'] + "&q=intitle:" + str(query) + "&startIndex=" + str((page - 1 ) * 10))
    return response
def request_search_books_by_genre(genre, page=1):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?key=" + API_KEYS['google_books'] + "&q=subject:" + str(genre) + "&startIndex=" + str((page - 1 ) * 10))
    return response
def request_search_books_by_author(author, page=1):
    response = requests.get("https://www.googleapis.com/books/v1/volumes?key=" + API_KEYS['google_books'] + "&q=inauthor:" + str(author) + "&startIndex=" + str((page - 1 ) * 10))
    return response