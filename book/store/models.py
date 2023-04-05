from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255, default='F')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')

    def __str__(self):
        return f"Id: {self.id}: {self.name}"


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'So so'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveIntegerField(choices=RATE_CHOICES, default=None, null=True)

    def __str__(self):
        return f" {self.user.username}: {self.book.name}, Rating: {self.rate}"
