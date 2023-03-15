from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.serializers import BookSerializer


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
