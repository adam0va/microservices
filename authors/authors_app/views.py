from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authors_app.models import Author
from authors_app.serializers import AuthorSerializer


@api_view(['GET', 'POST'])
def authors_list(request):
    if request.method == 'GET':
        if len(request.query_params) == 0:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        name = request.query_params.get("name")
        surname = request.query_params.get("surname")
        if name is None:
            return Response({"error" : "no name in query params"}, status = status.HTTP_400_BAD_REQUEST)
        if surname is None:
            return Response({"error" : "no surname in query params"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            authors = Author.objects.filter(name=name, surname=surname)
            if len(authors) == 0:
                return Response(status = status.HTTP_404_NOT_FOUND)
            else:
                serializer = AuthorSerializer(authors, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
