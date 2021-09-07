# from rest_framework.test import APITestCase
# from ..models import Book
#
#
#
# class BookAPITestCase(APITestCase):
#     def test_book_api_list_view(self):
#         book = Book.objects.create(...)
#         response = self.client.get(
#             'api/booklist/',
#         )
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         list_of_ids = [obj.id for obj in data]
#         self.assertIn(book.id, list_of_ids)
#
#
# class BooksAPITestCase(APITestCase):
#     def test_book_api_list_view(self):
#         book = Book.objects.create(...)
#         response = requests.get(
#             'api/booklist/',
#         )
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         list_of_ids = [obj.id for obj in data]
#         self.assertIn(book.id, list_of_ids)