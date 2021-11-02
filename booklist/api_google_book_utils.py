from requests import get, post, codes, exceptions
# Request
from json import loads, dumps
import pprint
from json import loads
from datetime import date
import datetime

class BooksApiError(Exception):
    pass


class BooksImporterApiError(Exception):
    pass


class BooksPhraseApiError(Exception):
    pass


class NoDataApiError(Exception):
    pass


def url_builder(id_query, *args):
    DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
    url_query = f'{DEFAULT_URL}{id_query}'
    if len(args) > 0:
        for arg in args:
            url_query = f'{url_query}{arg}'
    return url_query


def prepare_list_of_json_to_bulk_create(object_books_from_api):
    object_books_api = object_books_from_api.get('items', '')
    if not object_books_api:
        print('noo items, no books, return is empty')
        return []
    list_of_dict_proper_books = []
    counter = 0
    for book in object_books_api:
        counter += 1
        publishedDate = book.get("volumeInfo", {}).get('publishedDate', '')
        # tutaj jesli jest pusty to omijamy
        if not publishedDate:
            continue
        volume_info = book.get("volumeInfo")
        industryIdentifiers = volume_info.get('industryIdentifiers', '')
        if not industryIdentifiers:
            continue
        for type_identifier in industryIdentifiers:
            if type_identifier.get('type') == 'ISBN_13':
                print(' we have type of isbn 13')
                isbn_13 = type_identifier.get('identifier')
                print('this is value of isbn13 type from identifier:\n', isbn_13)

                # tu musi byc checker ktory sprawdzi czy isbn ma 13 znakow i czy sa w nich litery i cyfry
                thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')

            # else:
            #     isbn_13 = 'dupa'

                # 3 tu musi byc spliter listy i zamiana na str join ze splitem po , lub ;
                book_to_add = {"title": volume_info.get('title'),
                               "authors": volume_info.get('authors'),
                               "publishedDate": volume_info.get('publishedDate'),
                               "isbn_13": isbn_13,
                               "pageCount": volume_info.get('pageCount'),
                               "language": volume_info.get('language'),
                               "link_book_cover": thumbnail,
                               }
                list_of_dict_proper_books.append(book_to_add)
                # I need to leave from this spin of loop because I got proper record so I go to next book
                break
            else:
                continue

        # try:
        #     volume_info = book['volumeInfo']
        #     if volume_info.get('publishedDate'):
        #         for type_identifier in volume_info.get('industryIdentifiers'):
        #             if type_identifier.get('type') == 'ISBN_13':
        #                 if volume_info.get('imageLinks'):
        #                     thumbnail = volume_info.get('imageLinks').get('thumbnail')
        #                 else:
        #                     thumbnail = None
        #                 book_to_add = {"title": volume_info.get('title'),
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

    if len(list_of_dict_proper_books) > 0:
        return list_of_dict_proper_books
    else:
        return []

def is_intiger(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def spliter_list_into_stings(object_list):
    # https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
    if len(object_list) > 1:
        str.split(object_list, sep=[',', ';'])


class BooksImporterApi:
    def __init__(self, phrase):
        self.phrase = phrase
        self.objects = []
        self.objects_books = []
        self.data = ''
        self.url = ''
        self.error = ''

    def run(self):
        # 1. get resposne from google
        self.url_builder()
        self.ask_api_for_phrase_data()
        self.data_items_exist_checker()
        # 2. Parse response to objects
        # 3. return amoutn of cretaed books

    def how_many_objects(self):
        return len(self.objects)

    def url_builder(self):
        DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
        self.url = f'{DEFAULT_URL}{self.phrase}'

    def ask_api_for_phrase_data(self):
        url = self.url
        response = get(url)
        if response.status_code != 200:
            self.error = response.status_code
            if response.json().get("error").get("message") == 'Missing query.':
                raise BooksPhraseApiError(
                    f'Error: you typed wrong phrase, try againe and change phrase to import books !')
            raise BooksImporterApiError(
                f'Couldnt connect\n Error: '
                f'{response.json().get("error").get("message")} , status code: {response.status_code}')
        try:
            len(loads(response.text).get('items'))
        except:
            raise NoDataApiError('no records from that phrase please try again')
        self.data = response.json()


    def data_items_exist_checker(self):
        counter = 0
        # ta czesc jest sprawdzona w glownym programie i jesli nie ma self.data.get.items to nie wywoluje klasu
        # if not self.data.get('items', ''):
        #     print('noo items, no books, return is empty')
        #     self.objects = []
        #     return



        # Kamil potrzebuje usystematyzowac nazewnictwo, zmiennych klas, parametrow, atrybutów, argumentow funkcji etc.
        # czy to jest ok industryIdentifiers jako zmienna ktora przechowuje wartosc slownika
        # Kamil czy to ma sens? jak to polaczyc z dziennikiem logów albo błędów?
        # if not self.data.get('items'):
        #     return NoDataApiError('Data delivered are wrong')
        for book in self.data.get('items'):
            counter += 1
            publishedDate = book.get("volumeInfo", {}).get('publishedDate', '')

            # czy da sie tutaj zastosowac konstrukcje z elif zeby to polaczyc w 1 ifa ?
            if not publishedDate:
                continue
            if len(publishedDate) == 4:
                if is_intiger(publishedDate):
                    publishedDate = datetime.date(int(publishedDate), 1, 1)
                else:
                    continue
            elif len(publishedDate) == 7:
                year = str.split(publishedDate, sep='-')[0]
                month = str.split(publishedDate, sep='-')[1]

                if is_intiger(year) and is_intiger(month):
                    publishedDate = datetime.date(int(year), int(month), 1)
                else:
                    continue
            elif len(publishedDate) == 10:
                year = str.split(publishedDate, sep='-')[0]
                month = str.split(publishedDate, sep='-')[1]
                day = str.split(publishedDate, sep='-')[2]
                if is_intiger(year) and is_intiger(month) and is_intiger(day):
                    publishedDate = datetime.date(int(year), int(month), int(day))
                else:
                    continue
            else:
                continue
            volume_info = book.get("volumeInfo", '')
            if not volume_info:
                continue
            industryIdentifiers = volume_info.get('industryIdentifiers', '')
            # sprawdzic czy to zadziala continue if not industryIdentifiers
            if not industryIdentifiers:
                continue
            for type_identifier in industryIdentifiers:
                if type_identifier.get('type') == 'ISBN_13':
                    thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
                    # ----------------------------------
                    # spr czy jest isdecimal i czy ma 13 znakow
                    isbn_13 = type_identifier.get('identifier', None)
                    if not len(isbn_13) == 13 and not str.isdecimal(isbn_13):
                        break
                    thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
                    print(thumbnail, ' thumbnail')
                    language = volume_info.get('language', '')
                    print(language, ' language')
                    if volume_info.get('pageCount', '') and is_intiger(volume_info.get('pageCount', '')):
                        pageCount = int(volume_info.get('pageCount'))
                    else:
                        pageCount = None
                        print('none pagecount')
                    authors = volume_info.get('authors', '')
                    if isinstance(authors, list):
                        pass

                    # authors_name: ['dr Hardwick', 'prof. K. McCoy']
                # --------------------------------------------------------------

                    # --------------------------------------------------------------

                    # print(self.objects, '  self object')
                    book_to_add = {
                        "title": volume_info.get('title'),
                        "authors": authors,
                        "publishedDate": publishedDate,
                        "isbn_13": isbn_13,
                        "pageCount": pageCount,
                        "language": language,
                        "link_book_cover": thumbnail,
                    }
                    print('book to add', book_to_add, 'type ', type(book_to_add))
                    self.objects.append(book_to_add)
                    break
                else:
                    continue




            # volume_info = book['volumeInfo']
            # if not volume_info.get('publishedDate'):
            #     continue
            # publishedDate = volume_info.get('publishedDate')







