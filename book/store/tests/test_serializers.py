from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer
from django.db.models import Count, Case, When, Avg


class BookSerializerTestCase(TestCase):

    def test_ser(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        book1 = Book.objects.create(name='Test book 1', price=25, author='F')
        book2 = Book.objects.create(name='Test book 2', price=55, author='F')

        UserBookRelation.objects.create(user=user1, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book1, like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=book2, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
            ).order_by('id')

        data = BookSerializer(books, many=True).data
        rate = 4.50
        rate1 = 4.67
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author': 'F',
                # 'owner': None,
                # 'readers': [],
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': "{:.2f}".format(rate1),
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author': 'F',
                # 'owner': None,
                # 'readers': [],
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': "{:.2f}".format(rate),
            }
        ]

        self.assertEqual(expected_data, data)
