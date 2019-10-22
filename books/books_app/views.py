from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from books_app.models import Book
from books_app.serializers import BookSerializer


@api_view(['GET', 'POST'])
def books_list(request):
    if request.method == 'GET':
        if len(request.query_params) == 0:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        title = request.query_params.get("title")
        if title is None:
            return Response({"error" : "no title in query params"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            books = Book.objects.filter(title=title)
            if len(books) == 0:
                return Response(status = status.HTTP_404_NOT_FOUND)
            else:
                serializer = BookSerializer(books, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)