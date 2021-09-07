from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Book
# Create your tests here.


class BooksViewsTestCase(TestCase):

    def test_book_list_view(self):
        url = reverse('booklist:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


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
