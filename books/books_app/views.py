from rest_framework import status
from rest_framework.views import Response, Request, APIView
from books_app.models import Book
from books_app.serializers import BookSerializer
from rest_framework.generics import ListCreateAPIView
#from rest_framework.renderers import JSONRenderer

class BookList(ListCreateAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        return Book.objects.all()
'''
class BookList(APIView):
    def get(self, request):
        if len(request.query_params) == 0:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'wrong request'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

class BookDetail(APIView):
    def get(self, request, uuid):
        try:
            book = Book.objects.get(pk=uuid)
        except Book.DoesNotExist:
            return Response({'error' : 'wrong query parameters'}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = BookSerializer(book)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def patch(self, request, uuid):
        try: 
            book = Book.objects.get(pk=uuid)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
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
        
