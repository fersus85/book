import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.db.models import Count, Case, When, Avg
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        self.book1 = Book.objects.create(name='Test book 1', price=25, author='author1', owner=self.user1)
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='author5')
        self.book3 = Book.objects.create(name='Test book author1', price=35, author='author2')
        self.count = len(Book.objects.all())

        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True)

        UserBookRelation.objects.create(user=self.user1, book=self.book2, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, like=True)
        UserBookRelation.objects.create(user=self.user3, book=self.book2, like=False)

        self.books = Book.objects.all().annotate(annotated_likes=Count(
            Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')

    def test_get(self):

        url = reverse('book-list')

        response = self.client.get(url)
        serializer_data = BookSerializer(self.books, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_filter(self):

        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book1.id, self.book3.id]).annotate(annotated_likes=Count(
            Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        response = self.client.get(url, data={'search': 'author1'})
        serializer_data = BookSerializer(books, many=True).data

        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_sorted(self):
        url = reverse('book-list')
        books = Book.objects.all().annotate(annotated_likes=Count(
            Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('price')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create(self):

        url = reverse('book-list')
        self.client.force_login(self.user1)
        data = {
            'name': 'Programming with Python',
            'price': '180.00',
            'author': 'Mark Summerfield'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user1, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        self.client.force_login(self.user1)
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
        self.client.force_login(self.user1)
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


class BooksRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.book1 = Book.objects.create(name='Test book 1', price=25, author='author1', owner=self.user,)
        self.book2 = Book.objects.create(name='Test book 2', price=55, author='author5')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)
        self.assertTrue(relation.like)
