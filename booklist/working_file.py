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