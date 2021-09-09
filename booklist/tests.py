from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from .models import Book
from . import views
# Create your tests here.


class BooksViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.book_1 = Book.objects.create(
            title='test123456',
            authors_name='test_author',
            published_date='2017-03-14',
            language_book='pl',
            link_book_cover='',
            page_number=0,
            isbn13_number=0
        )
        self.index_url = reverse('booklist:index')
        self.filter_search_order_url = reverse('booklist:filter_search_order')
        self.books_import_url = reverse('booklist:books_import')
        self.book_detail_url = reverse('booklist:book_detail', args=[self.book_1.id, ])
        self.book_update_url = reverse('booklist:book_update', args=[self.book_1.id, ])
        self.book_delete_url = reverse('booklist:book_delete', args=[self.book_1.id, ])
        self.book_add_url = reverse('booklist:book_add')
        # ------------------
        self.response_index = self.client.get(self.index_url)
        self.response_filter_search_order = self.client.get(self.filter_search_order_url)
        self.response_books_import = self.client.get(self.books_import_url)
        self.response_book_detail = self.client.get(self.book_detail_url)
        self.response_book_update = self.client.get(self.book_update_url)
        self.response_book_delete = self.client.get(self.book_delete_url)
        self.response_book_add = self.client.get(self.book_add_url)




    def test_index_view_status200(self):
        self.assertEqual(self.response_index.status_code, 200)

    def test_index_view_proper_html(self):
        self.assertTemplateUsed(self.response_index, 'booklist/index.html')

    def test_filter_search_order_view_status200(self):
        self.assertEqual(self.response_filter_search_order.status_code, 200)

    def test_index_view_proper_html(self):
        self.assertTemplateUsed(self.response_filter_search_order, 'booklist/filter_search.html')

    def test_books_import_view_status200(self):
        self.assertEqual(self.response_books_import.status_code, 200)

    def test_books_import_view_proper_html(self):
        self.assertTemplateUsed(self.response_books_import, 'booklist/import_phrase.html')

    def test_book_detail_view_status200(self):
        self.assertEqual(self.response_book_detail.status_code, 200)

    def test_book_detail_view_proper_html(self):
        self.assertTemplateUsed(self.response_book_detail, 'booklist/book_detail.html')

    def test_book_update_view_status200(self):
        self.assertEqual(self.response_book_update.status_code, 200)

    def test_book_update_view_proper_html(self):
        self.assertTemplateUsed(self.response_book_update, 'booklist/book_update_form.html')

    def test_book_delete_view_status200(self):
        self.assertEqual(self.response_book_delete.status_code, 200)

    def test_book_delete_view_proper_html(self):
        self.assertTemplateUsed(self.response_book_delete, 'booklist/delete_book.html')

    def test_book_add_view_status200(self):
        self.assertEqual(self.response_book_add.status_code, 200)

    def test_book_add_view_proper_html(self):
        self.assertTemplateUsed(self.response_book_add, 'booklist/book_create_form.html')


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
