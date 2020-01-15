from rest_framework import status
from rest_framework.views import Response, Request, APIView
from books_app.models import Book
from books_app.serializers import BookSerializer
from rest_framework.generics import ListCreateAPIView


class BookList(ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all()

    def post(self, request):
        data = request.data
        if data['reader_uuid'] == '':
            data['reader_uuid'] = None
        if data['author_uuid'] == '':
            data['author_uuid'] = None
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    def get(self, request, uuid):
        try:
            book = Book.objects.get(pk=uuid)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def patch(self, request, uuid):
        try: 
            book = Book.objects.get(pk=uuid)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        data = request.data
        if data['reader_uuid'] == '':
            data['reader_uuid'] = None
        if data['author_uuid'] == '':
            data['author_uuid'] = None
        serializer = BookSerializer(instance=book, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print('---')
            print(serializer.data)
            print('---')
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        try:
            book = Book.objects.get(pk=uuid)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
