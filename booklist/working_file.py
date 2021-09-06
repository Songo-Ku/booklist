from requests import get, post
from json import loads

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