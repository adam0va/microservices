from rest_framework import status
from rest_framework.views import Response, Request, APIView
from readers_app.models import Reader
from readers_app.serializers import ReaderSerializer

class ReaderList(APIView):
    def get(self, request):
        if len(request.query_params) == 0:
            readers = Reader.objects.all()
            serializer = ReaderSerializer(readers, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({'error': 'wrong request'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        serializer = ReaderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReaderDetail(APIView):
    def get(self, request, uuid):
        try:
            reader = Reader.objects.get(pk=uuid)
        except Reader.DoesNotExist:
            return Response({'error' : 'wrong query parameters'}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = ReaderSerializer(reader)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def patch(self, request, uuid):
        try: 
            reader = Reader.objects.get(pk=uuid)
        except Reader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReaderSerializer(instance=reader, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, uuid):
        try:
            reader = Reader.objects.get(pk=uuid)
        except Reader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reader.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
