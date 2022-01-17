from django.shortcuts import render, redirect
from .forms import SearchForm, CreateTopic
import math
from .requests import *
from .models import Topic
from django.contrib.auth.decorators import login_required

@login_required
def topic(request, item_type, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if item_type == 'movies':
        response = request_movie(topic.id_parent_item)
        if(response.status_code == 200):
            response = response.json()
            about = {'id': response['id'], 'title': response['title'], 'poster_path': response['poster_path']}
            if about['poster_path'] is not None:
                about['poster_path'] = 'https://image.tmdb.org/t/p/w500/' + about['poster_path']
    elif item_type == 'tv':
        response = request_tv(topic.id_parent_item)
        if(response.status_code == 200):
            response = response.json()
            about = {'id': response['id'], 'title': response['name'], 'poster_path': response['poster_path']}
            if about['poster_path'] is not None:
                about['poster_path'] = 'https://image.tmdb.org/t/p/w500/' + about['poster_path']
    elif item_type == 'books':
        response = request_book(topic.id_parent_item)
        if(response.status_code == 200):
            response = response.json()
            about = {'id': response['id'], 'title': response['volumeInfo']['title']}
            try:
               about['poster_path'] = response['volumeInfo']['imageLinks']['thumbnail']
            except:
                pass

    return render(request, 'apis/topic.html', {'topic': topic, 'about': about, 'firebase_credentials': FIREBASE_CREDENTIALS})

@login_required
def create_topic(request, id_parent_item, parent_item_type):
    if request.method == 'POST':
        form = CreateTopic(request.POST)
        if form.is_valid():
            t = form.save()
            return redirect('apis:topic', t.parent_item_type, t.id)
    else:
        form = CreateTopic(initial={'id_parent_item': id_parent_item, 'parent_item_type': parent_item_type, 'user': request.user})

    return render(request, 'apis/create_topic.html', {'form': form, 'id_parent_item': id_parent_item, 'parent_item_type': parent_item_type})

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            type = form.cleaned_data['type']
            query = form.cleaned_data['query']

            results = []
            if type == 'movies':
                return redirect('search/movies?query=' + str(query))
            elif type == 'tv':
                return redirect('search/tv?query=' + str(query))
            elif type == 'books':
                return redirect('search/books?query=' + str(query))
            elif type == 'all':
                # Search movies
                response = request_search_movies(query)
                if(response.status_code == 200):
                    response = response.json()
                    if response['total_results'] > 0:
                        result = {}
                        result['type'] = 'movies'
                        result['type_name'] = 'Filmes'
                        result['results'] = []
                        for movie in response['results']:
                            result['results'].append({'id': movie['id'], 'title': movie['title'], 'poster_path': movie['poster_path']})
                            if result['results'][-1]['poster_path'] is not None:
                                result['results'][-1]['poster_path'] = 'https://image.tmdb.org/t/p/w500/' + result['results'][-1]['poster_path']
                        result['total_pages'] = response['total_pages']
                        results.append(result)

                # Search TV
                response = request_search_tv(query)
                if(response.status_code == 200):
                    response = response.json()
                    if response['total_results'] > 0:
                        result = {}
                        result['type'] = 'tv'
                        result['type_name'] = 'Séries'
                        result['results'] = []
                        for tv in response['results']:
                            result['results'].append({'id': tv['id'], 'title': tv['name'], 'poster_path': tv['poster_path']})
                            if result['results'][-1]['poster_path'] is not None:
                                result['results'][-1]['poster_path'] = 'https://image.tmdb.org/t/p/w500/' + result['results'][-1]['poster_path']
                        result['total_pages'] = response['total_pages']
                        results.append(result)
                
                # Search books
                response = request_search_book(query)
                if(response.status_code == 200):
                    response = response.json()
                    if response['totalItems'] > 0:
                        result = {}
                        result['type'] = 'books'
                        result['type_name'] = 'Livros'
                        result['results'] = []
                        for book in response['items']:
                            result['results'].append({'id': book['id'], 'title': book['volumeInfo']['title']})
                            try:
                                result['results'][-1]['poster_path'] = book['volumeInfo']['imageLinks']['thumbnail']
                            except:
                                pass
                        result['total_pages'] = math.ceil(response['totalItems'] / 10)
                        results.append(result)
                
            context = {"search_form": form, "query": query, "results": results}
            return render(request, 'apis/search.html', context)
    
    return redirect('my_site:index')

def search_type(request, type):
    page = 1
    if request.method == 'POST':
        query = request.POST['query']
        if 'page' in request.POST:
            page = request.POST['page']
    elif request.method == 'GET':
        query = request.GET['query']
    else:
        return redirect('my_site:index')

    page = int(page)

    if query is not None:
        result = {}
        if type == 'movies':
            response = request_search_movies(query, page)
            if(response.status_code == 200):
                result = response.json()
                result['available_pages'] = range(1, result['total_pages'] + 1)
        elif type == 'tv':
            response = request_search_tv(query, page)
            if(response.status_code == 200):
                result = response.json()
                result['available_pages'] = range(1, result['total_pages'] + 1)
        elif type == 'books':
            response = request_search_book(query, page)
            if(response.status_code == 200):
                result = response.json()
                result['page'] = int(page)
                result['total_pages'] = math.ceil(result['totalItems'] / 10)
                result['available_pages'] = range(1, result['total_pages'] + 1)

        context = {"query": query, "result": result}
        return render(request, 'apis/' + type +  '/search_' + type +  '.html', context)
    else:
        return redirect('my_site:index')

#-----------------------------------------------------------------------------------------------------------------------
# Movies - Api The Movie Database(TMDB)

def search_movies_genre(request, page=1):
    page = 1
    if request.method == 'POST':
        genre_id = request.POST['query']
        if 'page' in request.POST:
            page = request.POST['page']
    elif request.method == 'GET':
        genre_id = request.GET['query']
    else:
        return redirect('my_site:index')

    genre = {}
    result = {}
    response = request_search_movies_by_genre(genre_id, page)
    if(response.status_code == 200):
        result = response.json()

        response = request_all_genres_movies()
        
        if(response.status_code == 200):
            genres = response.json()
            result['available_pages'] = range(1, result['total_pages'] + 1)
            
            for g in genres['genres']:
                if int(g['id']) == int(genre_id):
                    genre = g
                    break

    
    context = {"genre": genre, "result": result}
    return render(request, 'apis/movies/search_movies_genre.html', context)

def details_movie(request, movie_id):
    context = {}
    context['topics'] = Topic.objects.filter(parent_item_type="movies", id_parent_item=movie_id).order_by('-updated_at')
    response = request_movie(movie_id)
    if(response.status_code == 200):
        context["movie"] =  response.json()

    return render(request, 'apis/movies/details_movie.html', context)

#-----------------------------------------------------------------------------------------------------------------------
# TV - Api The Movie Database(TMDB)

def search_tv_genre(request, page=1):
    page = 1
    if request.method == 'POST':
        genre_id = request.POST['query']
        if 'page' in request.POST:
            page = request.POST['page']
    elif request.method == 'GET':
        genre_id = request.GET['query']
    else:
        return redirect('my_site:index')

    genre = {}
    result = {}
    response = request_search_tv_by_genre(genre_id, page)
    if(response.status_code == 200):
        result = response.json()

        response = request_all_genres_tv()
        
        if(response.status_code == 200):
            genres = response.json()
            result['available_pages'] = range(1, result['total_pages'] + 1)
            
            for g in genres['genres']:
                if int(g['id']) == int(genre_id):
                    genre = g
                    break

    context = {"genre": genre, "result": result}
    return render(request, 'apis/tv/search_tv_genre.html', context)

def details_tv(request, tv_id):
    context = {}
    context['topics'] = Topic.objects.filter(parent_item_type="tv", id_parent_item=tv_id).order_by('-updated_at')
    response = request_tv(tv_id)
    if(response.status_code == 200):
        context["tv"] =  response.json()

    return render(request, 'apis/tv/details_tv.html', context)

#-----------------------------------------------------------------------------------------------------------------------
# Books - Api Google Books

def search_books_genre(request, page=1):
    page = 1
    if request.method == 'POST':
        genre = request.POST['query']
        if 'page' in request.POST:
            page = request.POST['page']
    elif request.method == 'GET':
        genre = request.GET['query']
    else:
        return redirect('my_site:index')

    page = int(page)

    result = {}
    response = request_search_books_by_genre(genre, page)
    if(response.status_code == 200):
        result = response.json()
        result['page'] = int(page)
        result['total_pages'] = math.ceil(result['totalItems'] / 10)
        result['available_pages'] = range(1, result['total_pages'] + 1)

    context = {"genre": genre, "result": result}
    return render(request, 'apis/books/search_books_genre.html', context)

def search_books_author(request, page=1):
    page = 1
    if request.method == 'POST':
        author = request.POST['query']
        if 'page' in request.POST:
            page = request.POST['page']
    elif request.method == 'GET':
        author = request.GET['query']
    else:
        return redirect('my_site:index')

    page = int(page)

    result = {}
    response = request_search_books_by_author(author, page)
    if(response.status_code == 200):
        result = response.json()
        result['page'] = int(page)
        result['total_pages'] = math.ceil(result['totalItems'] / 10)
        result['available_pages'] = range(1, result['total_pages'] + 1)

    context = {"author": author, "result": result}
    return render(request, 'apis/books/search_books_author.html', context)

def details_book(request, book_id):
    context = {}
    context['topics'] = Topic.objects.filter(parent_item_type="books", id_parent_item=book_id).order_by('-updated_at')
    
    response = request_book(book_id)
    if(response.status_code == 200):
        context["book"] =  response.json()

    return render(request, 'apis/books/details_book.html', context)
        
