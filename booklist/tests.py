from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from .models import Book
from . import views
# Create your tests here.


class BooksViewsTestCase(TestCase):

    def test_index_view_status200(self):
        url = reverse('booklist:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_search_order_view_status200(self):
        url = reverse('booklist:filter_search_order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_books_import_view_status200(self):
        url = reverse('booklist:books_import')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_detail_view_status200(self):
        book = Book.objects.create(title='test123456',
                                   authors_name='test_author',
                                   published_date='2017-03-14',
                                   language_book='pl',
                                   link_book_cover='',
                                   page_number=0,
                                   isbn13_number=0)
        url = reverse('booklist:book_detail', args=[book.id, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_update_view_status200(self):
        book = Book.objects.create(title='test123456',
                                   authors_name='test_author',
                                   published_date='2017-03-14',
                                   language_book='pl',
                                   link_book_cover='',
                                   page_number=0,
                                   isbn13_number=0)
        url = reverse('booklist:book_update', args=[book.id, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_delete_view_status200(self):
        book = Book.objects.create(title='test123456',
                                   authors_name='test_author',
                                   published_date='2017-03-14',
                                   language_book='pl',
                                   link_book_cover='',
                                   page_number=0,
                                   isbn13_number=0)
        url = reverse('booklist:book_delete', args=[book.id, ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_add_view_status200(self):
        url = reverse('booklist:book_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('booklist:index')
        self.assertEquals(resolve(url).func.view_class, views.IndexView)

    def test_filter_search_ordering_url_is_resolved(self):
        url = reverse('booklist:filter_search_order')
        self.assertEquals(resolve(url).func.view_class, views.BookFilterSearchListView)

    def test_books_import_url_is_resolved(self):
        url = reverse('booklist:books_import')
        self.assertEquals(resolve(url).func.view_class, views.BookImportView)

    def test_book_detail_url_is_resolved(self):
        url = reverse('booklist:book_detail', args=[33, ])
        self.assertEquals(resolve(url).func.view_class, views.BookDetailView)

    def test_book_add_url_is_resolved(self):
        url = reverse('booklist:book_add')
        self.assertEquals(resolve(url).func.view_class, views.BookCreateView)

    def test_book_delete_url_is_resolved(self):
        url = reverse('booklist:book_delete', args=[33, ])
        self.assertEquals(resolve(url).func.view_class, views.BookDeleteView)

    def test_book_update_url_is_resolved(self):
        url = reverse('booklist:book_update', args=[33, ])
        self.assertEquals(resolve(url).func.view_class, views.BookUpdateView)








# class BookAPITestCase(APITestCase):
#     def test_book_api_list_view(self):
#         book = Book.objects.create()
#         response = self.client.get(
#             reverse('api-booklist:post-create')
#             # 'api/booklist/',
#         )
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         list_of_ids = [obj.id for obj in data]
#         self.assertIn(book.id, list_of_ids)
#
