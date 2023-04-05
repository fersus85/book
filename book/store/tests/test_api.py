import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book1 = Book.objects.create(name='Test book 1', price=25, author='author1', owner=self.user)
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='author5')
        self.book3 = Book.objects.create(name='Test book author1', price=35, author='author2')
        self.count = len(Book.objects.all())

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

    def test_create(self):

        url = reverse('book-list')
        self.client.force_login(self.user)
        data = {
            'name': 'Programming with Python',
            'price': '180.00',
            'author': 'Mark Summerfield'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        self.client.force_login(self.user)
        data = {
            'name': self.book1.name,
            'price': 80,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(80, self.book1.price)

    def test_delete(self):
        url = reverse('book-detail', args=(self.book1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        count = len(Book.objects.all())
        self.assertEqual(count, 2)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_update_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book1.id,))
        self.client.force_login(self.user2)
        data = {
            'name': self.book1.name,
            'price': 80,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(80, self.book1.price)
