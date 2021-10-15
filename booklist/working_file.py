<<<<<<< HEAD
from requests import get, post, codes, exceptions
from json import loads, dumps
import pprint
from django.shortcuts import (render, get_object_or_404, redirect,)
from django.urls import reverse, reverse_lazy
# from django.views import generic
from django.views.generic import (
	TemplateView,
	DetailView,
	CreateView,
	ListView,
	DeleteView,
	UpdateView
)
import sys
sys.path.append('.')
# ---------------------------------------
from .models import Book
from .forms import BookModelForm
from .filters import BooklistFilter
# ---------------------------------------
from requests import get, exceptions
from json import loads
# from .api_google_book_utils import prepare_list_of_json_to_bulk_create, url_builder
# ------------------------


def url_builder(id_query, *args):
    DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
    url_query = f'{DEFAULT_URL}{id_query}'
    if len(args) > 0:
        for arg in args:
            url_query = f'{url_query}{arg}'
    return url_query


phrase = 'robbinson'
url = url_builder(phrase)
response = get(url)
response = loads(response.text)

object_books_api = response.get('items')
list_of_dict_proper_books = []
counter = 0
for book in object_books_api:
    # book_number += 1
    # print(book_number)
    counter += 1
    volume_info = book['volumeInfo']
    # print('nie ma published date dla ', counter)
    if not volume_info.get('industryIdentifiers'):
        print('sztos nie ma daty\n')
    if not volume_info.get('publishedDate'):
        print('dupa nie ma identyfikatora industry \n')
    try:
        if volume_info.get('publishedDate'):

            # tutaj obsługa dat
            if volume_info.get('industryIdentifiers'):
                for type_identifier in volume_info.get('industryIdentifiers'):
                    if type_identifier.get('type') == 'ISBN_13':
                        if volume_info.get('imageLinks'):
                            thumbnail = volume_info.get('imageLinks').get('thumbnail')
                        else:
                            thumbnail = None
                        book_to_add = {"title": volume_info.get('title'),
                                       # 'id': book['id'],
                                       # "selfLink": book['selfLink'],
                                       "authors": volume_info.get('authors'),
                                       "publishedDate": volume_info.get('publishedDate'),
                                       "isbn_13": type_identifier.get('identifier'),
                                       "pageCount": volume_info.get('pageCount'),
                                       "language": volume_info.get('language'),
                                       "link_book_cover": thumbnail,
                                       }
                        list_of_dict_proper_books.append(book_to_add)
                        # I need to leave from this spin of loop because I got proper record so I go to next book
                        break
                    else:
                        isbn_13_identifier = ''
                        if volume_info.get('imageLinks'):
                            thumbnail = volume_info.get('imageLinks').get('thumbnail')
                        else:
                            thumbnail = None
                        book_to_add = {"title": volume_info.get('title'),
                                       # 'id': book['id'],
                                       # "selfLink": book['selfLink'],
                                       "authors": volume_info.get('authors'),
                                       "publishedDate": volume_info.get('publishedDate'),
                                       "isbn_13": isbn_13_identifier,
                                       "pageCount": volume_info.get('pageCount'),
                                       "language": volume_info.get('language'),
                                       "link_book_cover": thumbnail,
                                       }
                        list_of_dict_proper_books.append(book_to_add)

    except:
        print(f'nie bylo ksiazki {counter}')

list_of_dict_proper_books = []
counter = 0
for book in object_books_api:
    # book_number += 1
    # print(book_number)
    counter += 1
    volume_info = book['volumeInfo']
    # print('nie ma published date dla ', counter)
    if not volume_info.get('language'):
        print('sztos nie ma language\n')
    if not volume_info.get('pageCount'):
        print('dupa nie ma pageCount \n')


























    # try:
    #
    #     if  volume_info.get('publishedDate'):

    #         for type_identifier in volume_info.get('industryIdentifiers'):
    #             if type_identifier.get('type') == 'ISBN_13':
    #                 if volume_info.get('imageLinks'):
    #                     thumbnail = volume_info.get('imageLinks').get('thumbnail')
    #                 else:
    #                     thumbnail = None
    #                 book_to_add = {"title": volume_info.get('title'),
    #                                # 'id': book['id'],
    #                                # "selfLink": book['selfLink'],
    #                                "authors": volume_info.get('authors'),
    #                                "publishedDate": volume_info.get('publishedDate'),
    #                                "isbn_13": type_identifier.get('identifier'),
    #                                "pageCount": volume_info.get('pageCount'),
    #                                "language": volume_info.get('language'),
    #                                "link_book_cover": thumbnail,
    #                                }
    #                 list_of_dict_proper_books.append(book_to_add)
    #                 # I need to leave from this spin of loop because I got proper record so I go to next book
    #                 break
    # except:
    #     print(f'nie bylo ksiazki {counter}')






























object_books_api = get_data_from_google_api(url_builder('Hobbit'))
book_number = 0
if object_books_api.get('items'):
    object_books_api = object_books_api.get('items')
    list_with_proper_books = []
    for book in object_books_api:
        book_number += 1
        print(book_number)
        if book['volumeInfo']:
            if book['volumeInfo'].get('industryIdentifiers'):
                for type_identifier in book['volumeInfo'].get('industryIdentifiers'):
                    if type_identifier.get('type') == 'ISBN_13':
                        if book['volumeInfo'].get('imageLinks'):
                            thumbnail = book['volumeInfo'].get('imageLinks').get('thumbnail')
                        else:
                            thumbnail = None
                        book_to_add = {'id': book['id'],
                                       # "selfLink": book['selfLink'],
                                       "title": book['volumeInfo'].get('title'),
                                       "authors": book['volumeInfo'].get('authors'),
                                       "publishedDate": book['volumeInfo'].get('publishedDate'),
                                       "isbn_13": type_identifier.get('identifier'),
                                       "pageCount": book['volumeInfo'].get('pageCount'),
                                       "language": book['volumeInfo'].get('language'),
                                       "link_book_cover": thumbnail,
                                       }
                        list_with_proper_books.append(book_to_add)
                        print('dobra dupa')
                        break
                    else:
                        print('dupa bez isbn13')
            else:
                print('zła dupa')
        else:
            print(' no volume info')

else:
    print('no items')


prepare_json_to_bulk_create(object_books_api)
=======
from requests import get, post, codes, exceptions
from json import loads, dumps
import pprint
from django.shortcuts import (render, get_object_or_404, redirect,)
from django.urls import reverse, reverse_lazy
# from django.views import generic
from django.views.generic import (
	TemplateView,
	DetailView,
	CreateView,
	ListView,
	DeleteView,
	UpdateView
)
import sys
sys.path.append('.')
import datetime
# ---------------------------------------

# ---------------------------------------
from requests import get, exceptions
from json import loads
# from .api_google_book_utils import prepare_list_of_json_to_bulk_create, url_builder
# ------------------------
from datetime import date


class BooksImporterApiError(Exception):
    pass


class BooksPhraseApiError(Exception):
    pass


class NoDataApiError(Exception):
    pass


def is_intiger(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def url_builder(id_query, *args):
    DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
    url_query = f'{DEFAULT_URL}{id_query}'
    if len(args) > 0:
        for arg in args:
            url_query = f'{url_query}{arg}'
    return url_query




DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q=hobbit"
response = get(DEFAULT_URL)
response.json().get('error').get('message')
response.json()
loads(response.text)
    #     if not response.get('items'):
    #         return render(
    #             request,
    #             'booklist/import_failed.html',
    #             {'error_message': 'no information about that phrase'}
    #         )


class BooksApiError(Exception):
    pass


try:
    books_importer = BooksImporterApi('hobbit')
    books_importer.run()
except Exception as message:
    print(message)

objjj = {'title': 'The New Zealand Hobbit Crisis', 'authors': ['Jonathan Handel '], 'publishedDate': date(2012, 11, 22), 'isbn_13': '9780615731001', 'pageCount': 92, 'language': 'en', 'link_book_cover': 'http://books.google.com/books/content?id=RdiRAQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}
objjj.get('pageCount')
dej_no_dana.run()
dej_no_dana.phrase
dej_no_dana.objects
dej_no_dana.data

response.json()['items'][0].get('volumeInfo').get('pageCount')
if is_intiger(response.json()['items'][0].get('volumeInfo').get('pageCount')):
    print('dupa')


if not volume_info.get('pageCount'):
    pageCount = ''
else:
    pageCount = volume_info.get('pageCount')


response.json()['items'][5].get('volumeInfo').get('pageCount')




# trawisto vs travium
# 2 tab:
# mieta 100mg vs
# wyc lisc karczocha 240 mg
# wyc z owocow kopru 40 mgr
# wyc z ostrzyzu dlugiego 200 mg



































# Jeśli chodzi o minusy:
# - debug True na produkcji
# - brak datepickera do wybierania dat
# - nie udało mi się zawęźić wyników wyszukiwania używając dat publikacji
# - brak paginacji książęk
# - wyszukiwanie po stronie API działa inaczej niż w przypadku formularza - np.
# https://songoku.pythonanywhere.com/api/booklist/?id=&title=hobbit&authors_name=&language_book=
# (case insensitive)
# vs
# https://songoku.pythonanywhere.com/filter-search-ordering/?title__icontains=hobbit&authors_name__icontains=&language_book__icontains=&created__gt=&created__lt=&ordering=
# (case sensitive)
# - kod niezgodny z PEP8 np za dużo zagnieżdzonych instrukcji warunkowych, kolejność importów, nazewnictwo zmiennych/funkcji np prepare_listOfJson_to_bulk_create itp.
# - testy nie sprawdzają zbyt wiele
# - w setUp powinno być przygotowanie do testów - nie powinno się używać klienta API w metodzie setUp
# - bardzo dużo zakomentowanego kodu
# - nie da się uruchomić testów (IndentationError)
#
# Ran 1 test in 0.000s
#
# FAILED (errors=1)

from django.core.paginator import Paginator
objects = ['john', 'paul', 'george', 'ringo']
p = Paginator(objects, 2)
p.count
p.num_pages
p.page_range
page1 = p.page(1)
page1.object_list

page2 = p.page(2)
page2.object_list
page2.has_next()
page2.has_previous()
page2.has_other_pages()
page2.next_page_number()
page2.previous_page_number()
page2.start_index()
page2.end_index()



>>>>>>> 44f4f29735af525554edde251166c966b54bb304
