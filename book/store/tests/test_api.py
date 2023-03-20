from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):

    def setUp(self):
        self.book1 = Book.objects.create(name='Test book 1', price=25, author='author1')
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='author5')
        self.book3 = Book.objects.create(name='Test book author1', price=35, author='author2')

    def test_get(self):

        url = reverse('book-list')

        response = self.client.get(url)
        serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_filter(self):

        url = reverse('book-list')

        response = self.client.get(url, data={'search': 'author1'})
        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_sorted(self):
        url = reverse('book-list')

        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book1, self.book3, self.book2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
