from requests import get, post, codes, exceptions
# Request
from json import loads, dumps
import pprint


def url_builder(id_query, *args):
    DEFAULT_URL = "https://www.googleapis.com/books/v1/volumes?q="
    url_query = f'{DEFAULT_URL}{id_query}'
    if len(args) > 0:
        for arg in args:
            url_query = f'{url_query}{arg}'
    return url_query


def prepare_list_of_json_to_bulk_create(object_books_from_api):
    object_books_api = object_books_from_api.get('items')
    list_of_dict_proper_books = []
    counter = 0
    for book in object_books_api:
        # book_number += 1
        # print(book_number)
        counter += 1
        try:
            volume_info = book['volumeInfo']
            if volume_info.get('publishedDate'):
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
        except:
            print(f'nie bylo ksiazki {counter}')




    if len(list_of_dict_proper_books) > 0:
        return list_of_dict_proper_books
    else:
        return []



# def prepare_list_of_json_to_bulk_create(object_books_from_api):
#     object_books_api = object_books_from_api.get('items')
#     list_of_dict_proper_books = []
#     for book in object_books_api:
#         # book_number += 1
#         # print(book_number)
#         if book['volumeInfo']:
#             if book['volumeInfo'].get('industryIdentifiers'):
#                 for type_identifier in book['volumeInfo'].get('industryIdentifiers'):
#                     if type_identifier.get('type') == 'ISBN_13':
#                         if book['volumeInfo'].get('imageLinks'):
#                             thumbnail = book['volumeInfo'].get('imageLinks').get('thumbnail')
#                         else:
#                             thumbnail = None
#                         book_to_add = {"title": book['volumeInfo'].get('title'),
#                                        # 'id': book['id'],
#                                        # "selfLink": book['selfLink'],
#                                        "authors": book['volumeInfo'].get('authors'),
#                                        "publishedDate": book['volumeInfo'].get('publishedDate'),
#                                        "isbn_13": type_identifier.get('identifier'),
#                                        "pageCount": book['volumeInfo'].get('pageCount'),
#                                        "language": book['volumeInfo'].get('language'),
#                                        "link_book_cover": thumbnail,
#                                        }
#                         list_of_dict_proper_books.append(book_to_add)
#                         # I need to leave from this spin of loop because I got proper record so I go to next book
#                         break
#     if len(list_of_dict_proper_books) > 0:
#         return list_of_dict_proper_books
#     else:
#         return []

