from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ser(self):
        book1 = Book.objects.create(name='Test book 1', price=25, author='F')
        book2 = Book.objects.create(name='Test book 2', price=55, author='F')
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author': 'F',
                'owner': None,
                'readers': []
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author': 'F',
                'owner': None,
                'readers': []
            }
        ]
        # print(data)
        # print(expected_data)
        self.assertEqual(expected_data, data)
