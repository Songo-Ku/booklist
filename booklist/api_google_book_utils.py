from requests import get, post, codes, exceptions
# Request
from json import loads, dumps
import pprint


# def response_token_public_api(url, login_data):
#     response = post(url, data=login_data)
#     if response.status_code == codes.ok:
#         print('tutaj trzeba zwrocic formule ktora by zabezpieczyla przed dalszym wlaczeniem programu gdy brak tokenu')
#         return loads(response.text)['token']
#     else:
#         print('zwroc blad')
#         return 'failed'
#

# # return response with data ready to use.
# def get_data_from_query(url, auth_key):
#     headers = {'Authorization': auth_key}
#     response = get(url=url, headers=headers)
#     try:
#         response.raise_for_status()
#     except exceptions.HTTPError as e:
#         # Whoops it wasn't a 200
#         return "Error: " + str(e)
#     if response.status_code == codes.ok:
#         return loads(response.text).get("data")
#     else:
#         print('zwroc blad')
#         return 'failed'
#
#
# def json_filter_fields(response, set_to_out):
#     number_record = 0
#     for record in response:
#         delete = [key for key in record if key in set_to_out]
#             # mozliwe ze trzeba dodac jeszcze ifa > 0 delete
#         for key in delete:
#             # delete key from unique record
#             removed_key = record.pop(key)
#             #  reassign record in each record
#         response[number_record] = record
#         number_record += 1
#     return response
#
#
# def get_data(sid_auth, sid_sig, from_date, to_date, sid):
#     URL = 'https://conversionlabs.net.pl/statistic/website-daily-visits?from='
#     get_response = get(
#         f'{URL}{from_date}&to={to_date}&step=days&sid={sid}&nocache=true',
#         cookies={'sid': sid_auth, 'sid.sig': sid_sig}
#     )
#     try:
#         get_response.raise_for_status()
#     except exceptions.HTTPError as e:
#         print("Error: " + str(e))
#         return "failed"
#
#     return loads(get_response.text).get("data")
#

def url_builder(id_query, *args):
    DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
    url_query = f'{DEFAULT_URL}{id_query}'
    if len(args) > 0:
        for arg in args:
            url_query = f'{url_query}{arg}'
    return url_query


def get_data_from_google_api(url):
    get_response = get(f'{url}')
    try:
        get_response.raise_for_status()
    except exceptions.HTTPError as e:
        print("Error: " + str(e))
        return "failed"
    return loads(get_response.text)


def prepare_json_to_bulk_create(object_books_from_api):
    if object_books_from_api.get('items'):
        object_books_api = object_books_from_api.get('items')
        listOfDict_proper_books = []
        for book in object_books_api:
            # book_number += 1
            # print(book_number)
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
                            listOfDict_proper_books.append(book_to_add)
                            # I need to leave from this spin of loop because I got proper record so I go to next book
                            break
        if len(listOfDict_proper_books) > 0:
            return listOfDict_proper_books
        else:
            return []
    else:
        return []


