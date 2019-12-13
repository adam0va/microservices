from rest_framework import status
from rest_framework.views import Response, Request, APIView
from authors_app.models import Author
from authors_app.serializers import AuthorSerializer
from rest_framework.generics import ListCreateAPIView


class AuthorList(ListCreateAPIView):
    serializer_class = AuthorSerializer
    def get_queryset(self):
        return Author.objects.all()
'''
class AuthorList(APIView):
    def get(self, request):
        if len(request.query_params) == 0:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'wrong request'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


class AuthorDetail(APIView):
    def get(self, request, uuid):
        try:
            author = Author.objects.get(pk=uuid)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def patch(self, request, uuid):
        try: 
            author = Author.objects.get(pk=uuid)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(instance=author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, uuid):
        try:
            author = Author.objects.get(pk=uuid)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        









