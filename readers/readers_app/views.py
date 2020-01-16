from rest_framework import status
from rest_framework.views import Response, Request, APIView
from readers_app.models import Reader
from readers_app.serializers import ReaderSerializer
from rest_framework.generics import ListCreateAPIView


class ReaderList(ListCreateAPIView):
    serializer_class = ReaderSerializer
    def get_queryset(self):
        return Reader.objects.all()


class ReaderDetail(APIView):
    def get(self, request, uuid):
        try:
            reader = Reader.objects.get(pk=uuid)
        except Reader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
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
            reader = Reader.objects.get(uuid=uuid)
        except Reader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reader.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
