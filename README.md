# webservices-trabalho-individual
## _COMMUNITY_

O Community é um projeto entreguem como trabalho individual da disciplina de WEBSERVICES, e se trata de uma site onde os usuários podem pesquisar e obter informações de filmes, livros e séries. O site também permite que após o usuário selecionar e entrar na página de cada um desses itens ele também possa ver e criar tópicos para discussões.

* Para a consulta de filmes e séries o projeto utiliza a api do The Movie Database([TMDB](https://www.themoviedb.org/)).
* Para a consulta de livros o projeto utiliza a api do [Google Books](https://developers.google.com/books/docs/overview).
* Para o armazenamento das mensagens dos tópicos o projeto utiliza o banco de dados [Firebase](https://firebase.google.com/).

## Utilização
* É recomendado que se esteja em um ambiente virtual para a execução do projeto.
* Para a execução do projeto é necessário ter o [Python3](https://www.python.org/downloads/) instalado. 
* Também é necessário ter o [pip](https://pip.pypa.io/en/stable/) instalado.

1. Baixe e descompacte o projeto no seu computador.
2. Instale os módulos necessários.
```
pip install -r requirements.txt
```
3. Insira suas chaves de acesso das APIs no arquivo [.env](community/community/.env).
4. Execute o projeto.
```
python community/manage.py runserver
```
5. Acesse o site no seu navegador no endereço [http://localhost:8000/](http://localhost:8000/).

# Capturas de Tela do Projeto
![Pesquisar](community/community/screenshots/search.png)
![Pesquisar_Livros](community/community/screenshots/search_books.png)
![Detalhes_Filme](community/community/screenshots/details_movie.png)
![Lista_de_Tópicos](community/community/screenshots/topics_list.png)
![Entrar](community/community/screenshots/login.png)