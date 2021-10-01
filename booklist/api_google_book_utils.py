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


def is_intiger(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


class BooksImporterApi:
    def __init__(self, phrase):
        self.phrase = phrase
        self.objects = []
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
        if not self.data.get('items'):
            return NoDataApiError('Data delivered are wrong')
        for book in self.data.get('items'):
            counter += 1
            volume_info = book['volumeInfo']
            if not volume_info.get('publishedDate'):
                continue
            publishedDate = volume_info.get('publishedDate')
            print('publishedDate: ', publishedDate)

            if len(publishedDate) == 4:
                print(' jest 4', publishedDate)
                print('is integer ', is_intiger(publishedDate))
                if is_intiger(publishedDate):
                    publishedDate = datetime.date(int(publishedDate), 1, 1)
                    print('date after datetype', publishedDate)
                else:
                    print('to sie wyswietla bo nie jest integer')
                    continue
            elif len(publishedDate) == 7:
                year = str.split(publishedDate, sep='-')[0]
                month = str.split(publishedDate, sep='-')[1]
                print('jest 7')
                if is_intiger(year) and is_intiger(month):
                    publishedDate = datetime.date(int(year), int(month), 1)
                    print('is integer ', is_intiger(year), is_intiger(month))
                    print('date after datetype', publishedDate)

                else:
                    print('to sie wyswietla bo nie jest integer')
                    continue
            elif len(publishedDate) == 10:
                print('jest 10')
                year = str.split(publishedDate, sep='-')[0]
                month = str.split(publishedDate, sep='-')[1]
                day = str.split(publishedDate, sep='-')[2]
                if is_intiger(year) and is_intiger(month) and is_intiger(day):
                    publishedDate = datetime.date(int(year), int(month), int(day))
                    print('is integer ', is_intiger(year), is_intiger(month), is_intiger(day))
                else:
                    print('to sie wyswietla bo nie jest integer')
                    continue
            else:
                continue
            isbn_13 = ''
            print('before isbn13')
            if volume_info.get('industryIdentifiers'):
                for identyficator_isbn in volume_info.get('industryIdentifiers'):
                    print('wszedl w petle isbn')
                    if identyficator_isbn.get('type') == 'ISBN_13' and \
                            is_intiger(identyficator_isbn.get('identifier')):
                        print('is integer and has isbn')
                        isbn_13 = int(identyficator_isbn.get('identifier'))
                        break
            print('before thumbnail')
            print(isbn_13)
            thumbnail = '' if not volume_info.get('imageLinks') else volume_info.get('imageLinks').get('thumbnail')
            print(thumbnail, ' thumbnail')
            if not volume_info.get('language'):
                language = ''
            else:
                language = volume_info.get('language')
            print(language, ' language')

            if volume_info.get('pageCount'):
                print('dupa dupa')
            if volume_info.get('pageCount') and is_intiger(volume_info.get('pageCount')):
                pageCount = int(volume_info.get('pageCount'))
            else:
                pageCount = ''
                print('pusty string')
            print(pageCount, ' pageCount')
            if not volume_info.get('authors'):
                authors = ''
            else:
                authors = volume_info.get('authors')
            print(pageCount, 'pagecouint')

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
            print(self.objects, '  self object')

