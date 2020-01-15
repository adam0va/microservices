from rest_framework import status
from rest_framework.views import Response, Request, APIView
from authors_app.models import Author
from authors_app.serializers import AuthorSerializer
from rest_framework.generics import ListCreateAPIView
from .permissions import BearerPermission
from django.contrib.auth.models import User

SERVER_ID = 'Authors_id'
SERVER_SECRET = 'Authors_secret'

class AuthorList(ListCreateAPIView):
    serializer_class = AuthorSerializer
    permission_classes = (BearerPermission,)

    def get_queryset(self):
        return Author.objects.all()


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
        

class GetServerToken(APIView):
    def _refresh(self, request: Request, us):
        import datetime
        from oauth2_provider.models import AccessToken, RefreshToken, Application
        from oauthlib import common
        ref_tok = request.data['refresh_token']
        try:
            refresh_token = RefreshToken.objects.get(token=ref_tok)
            app = Application.objects.get(name='Gateway')
        except RefreshToken.DoesNotExist:
            return Response({'error': 'Refresh token is not valid'}, status=status.HTTP_403_FORBIDDEN)
        except Application.DoesNotExist:
            return Response({'error': 'App is no longer exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        refresh_token.delete()
        old_token = refresh_token.access_token
        old_token.delete()
        new_token = AccessToken.objects.create(user=us, application=app, token=common.generate_token(),
                                               expires=datetime.datetime.now() + datetime.timedelta(minutes=30))
        new_refresh_token = RefreshToken.objects.create(user=us, application=app, token=common.generate_token(),
                                                        access_token=new_token)
        refresh_token.access_token = new_token
        return Response({
            'token': new_token.token,
            'type': 'BEARER',
            'expires_in': new_token.expires,
            'refresh_token': new_refresh_token.token,
        }, status=200)

    def _get(self, request: Request, us):
        from oauth2_provider.models import AccessToken, RefreshToken, Application
        from oauthlib import common
        import datetime
        try:
            app = Application.objects.get(name='Gateway')
        except Application.DoesNotExist:
            return Response({'error': 'App is no longer exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            access_token = AccessToken.objects.get(user=us)
            refresh_token = RefreshToken.objects.get(access_token=access_token)
        except AccessToken.DoesNotExist:
            access_token = AccessToken.objects.create(user=us, application=app, token=common.generate_token(),
                                                      expires=datetime.datetime.now() + datetime.timedelta(
                                                          minutes=30))
            refresh_token = RefreshToken.objects.create(user=us, application=app, access_token=access_token,
                                                        token=common.generate_token())
        except RefreshToken.DoesNotExist:
            refresh_token = RefreshToken.objects.create(user=us, application=app, access_token=access_token,
                                                        token=common.generate_token())
        return Response({
            'token': access_token.token,
            'type': 'BEARER',
            'expires_in': access_token.expires,
            'refresh_token': refresh_token.token,
        }, status=200)

    def post(self, request: Request):
        data = request.data

        try:
            sid = data['server_id']
            ssec = data['server_secret']
        except KeyError:
            return Response({'error': 'No server_id or server_secret in body'}, status=400)
        if sid != SERVER_ID or ssec != SERVER_SECRET:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username='Gateway')
        try:
            ref_tok = data['refresh_token']
            return self._refresh(request, user)
        except KeyError:
            return self._get(request, user)







