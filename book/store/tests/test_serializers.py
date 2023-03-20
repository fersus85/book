from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ser(self):
        book1 = Book.objects.create(name='Test book 1', price=25)
        book2 = Book.objects.create(name='Test book 2', price=55)
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author': 'F',
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author': 'F',
            }
        ]
        self.assertEqual(expected_data, data)
