from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from apis.forms import SearchForm

# Create your views here.
#@login_required
def index(request):

    search_form = SearchForm()
    return render(request, 'my_site/index.html', {"search_form": search_form})