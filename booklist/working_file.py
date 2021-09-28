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
from datetime import date


def url_builder(id_query, *args):
    DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
    url_query = f'{DEFAULT_URL}{id_query}'
    if len(args) > 0:
        for arg in args:
            url_query = f'{url_query}{arg}'
    return url_query


class BooksImporter:
    def __init__(self, phrase):
        self.phrase = phrase
        self.objects = {}
        self.data = {}

    def run(self):
        # 1. get resposne from google
        self.ask_api_for_phrase_data()
        # 2. Parse response to objects
        # 3. return amoutn of cretaed books

    def url_builder(self):
        DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
        url_query = f'{DEFAULT_URL}{self.phrase}'

        return url_query

    def ask_api_for_phrase_data(self):
        url = self.url_builder()
        response = get(url)
        if response.status_code != 200:
            raise BooksError(f'Couldnt connetc, status code {response.status_code}')
         self.data = loads(response.text)

    def data_items_exist_checker(self):

        ask_api_for_phrase_data(self)

        if not response.get('items'):
            return render(
                request,
                'booklist/import_failed.html',
                {'error_message': 'no information about that phrase'}
            )


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

    if not volume_info.get('publishedDate'):
        continue
    isbn_13 = ''
    if volume_info.get('industryIdentifiers'):
        for identyficator_isbn in volume_info.get('industryIdentifiers'):
            if identyficator_isbn.get('type')  == 'ISBN_13':
                isbn_13 = identyficator_isbn.get('identifier')
                break

    thumbnail = '' if not volume_info.get('imageLinks') else volume_info.get('imageLinks').get('thumbnail')

    if not volume_info.get('language'):
        language = ''
    else:
        language = volume_info.get('language')
    if not volume_info.get('pageCount'):
        pageCount = ''
    else:
        pageCount = volume_info.get('pageCount')
    if not volume_info.get('authors'):
        authors = ''
    else:
        authors = volume_info.get('authors')

    publishedDate = volume_info.get('publishedDate')
    publishedDate = '2009-01'

    d = date(2002, 12, 31)
    if len(publishedDate) == 4:
        publishedDate = date(int(publishedDate), 1, 1)
    elif len(publishedDate) == 7:

        year = str.split(publishedDate, sep='-')[0]
        month = str.split(publishedDate, sep='-')[1]
    if type(int(year)) == int:
        print(int(year))
        publishedDate = date(int(year), 1, 1)

    if isinstance(int(year), int):
        publishedDate = date(int(year), 1, 1)
        print(publishedDate)



    book_to_add = {"title": volume_info.get('title'),
                    "authors": authors,
                    "publishedDate": volume_info.get('publishedDate'),
                    "isbn_13": isbn_13,
                    "pageCount": pageCount,
                    "language": language,
                    "link_book_cover": thumbnail,
                    }
    list_of_dict_proper_books.append(book_to_add)













        for type_identifier in volume_info.get('industryIdentifiers'):
            if type_identifier.get('type') == 'ISBN_13':

                else:
                    thumbnail = None
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