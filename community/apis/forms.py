from tkinter import HIDDEN
from django import forms
from django.forms import ModelForm
from .models import Topic
from django.core.exceptions import ValidationError
from .requests import request_movie, request_tv, request_book
from users.models import User

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pesquisar'}))
    type = forms.ChoiceField(choices=[('all', 'Todos'), ('movies', 'Filmes'), ('books', 'Livros'), ('tv', 'Séries')])

    class Meta:
        fields = ['query', 'type']

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['query'].widget.attrs['class'] = 'form-control input-group-lg bg-dark text-white border-secondary rounded-pill me-2 px-4'
        self.fields['type'].widget.attrs['class'] = 'form-select form-select-lg bg-dark text-white text-center border-secondary rounded-pill'

class CreateTopic(ModelForm):
    id_parent_item = forms.CharField(max_length=32, widget=forms.HiddenInput())
    parent_item_type = forms.CharField(max_length=32, widget=forms.HiddenInput())
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Topic
        fields = ['title', 'description', 'id_parent_item', 'parent_item_type', 'user']

    def __init__(self, *args, **kwargs):
        super(CreateTopic, self).__init__(*args, **kwargs)

        self.fields['title'].label = "Título"
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].label = "Descrição"
        self.fields['description'].widget.attrs['class'] = 'form-control'
    
    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)

        data = self.id_parent_item
        if self.parent_item_type == 'movies':
            response = request_movie(data)
        if self.parent_item_type == 'tv':
            response = request_tv(data)
        if self.parent_item_type == 'books':
            response = request_book(data)
        else:
            raise ValidationError("Erro! O tópico não pode ser criado para este tipo de item.")

        if response.status_code != 200:
            raise ValidationError("Erro! O ID do item informado não existe.")
        return data
        
    def clean_parent_item_type(self):
        available_types = ['movies', 'tv', 'books']
        data = self.cleaned_data['parent_item_type']
        if data not in available_types:
            raise ValidationError("Erro! O tópico não pode ser criado para este tipo de item.")
        return data