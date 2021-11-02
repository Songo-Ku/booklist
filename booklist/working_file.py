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
    volume_info = book.get("volumeInfo", '')
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
































