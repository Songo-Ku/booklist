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