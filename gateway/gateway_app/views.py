from rest_framework.views import Response, Request, APIView
from .requesters.book_requester import BookRequester
from .requesters.reader_requester import ReaderRequester
from .requesters.author_requester import AuthorRequester
from .requesters.auth_requester import AuthRequester
from .permissions import IsAuthenticatedThroughAuthService
from django.shortcuts import render


def main_page(request):
    return render(request, "index.html")


class BaseAuthView(APIView):
    REQUESTER = AuthRequester()


class AuthView(BaseAuthView):
    def post(self, request):
        response_json, code = self.REQUESTER.authenticate(data=request.data)
        return Response(response_json, status=code)


class AllReadersView(APIView):
    permission_classes = (IsAuthenticatedThroughAuthService,)

    REQUESTER = ReaderRequester()

    def get(self, request):
        data, code = self.REQUESTER.get_all_readers(request=request)
        return Response(data, status=code)

    def post(self, request):
        data, code = self.REQUESTER.post_reader(request=request, data=request.data)
        return Response(data, status=code)


class ReaderView(APIView):
    permission_classes = (IsAuthenticatedThroughAuthService,)

    REQUESTER = ReaderRequester()

    def get(self, request, reader_uuid):
        data, code = self.REQUESTER.get_reader(request=request, uuid=reader_uuid)
        return Response(data, status=code)

    def delete(self, request, reader_uuid):
        data, code = self.REQUESTER.delete_reader(request=request,uuid=reader_uuid)
        return Response(data, status=code)

    def patch(self, request, reader_uuid):
        data, code = self.REQUESTER.patch_reader(request=request, uuid=reader_uuid, data=request.data)
        print(request.data)
        return Response(data, status=code)

TOKEN = ''
REFRESH = ''

class AllAuthorsView(APIView):
    REQUESTER = AuthorRequester()

    def _get_token(self, refresh=False):
        import requests
        global TOKEN, REFRESH
        body = {
            'server_id': 'Authors_id',
            'server_secret': 'Authors_secret',
        }
        if refresh:
            body['refresh_token'] = REFRESH
        ret = requests.post('http://127.0.0.1:8002/api/server_login/', json=body)
        print(f'response: {ret.json()}')
        TOKEN = ret.json()['token']
        REFRESH = ret.json()['refresh_token']

    def get(self, request):
        if TOKEN == '':
            self._get_token()
        data, code = self.REQUESTER.get_all_authors(request=request)
        if code == 403:
            self._get_token(refresh=True)
        data, code = self.REQUESTER.get_all_authors(request=request)
        return Response(data, status=code)

    def post(self, request):
        if TOKEN == '':
            self._get_token()
        data, code = self.REQUESTER.post_author(request=request, data=request.data)
        if code == 403:
            self._get_token(refresh=True)
        data, code = self.REQUESTER.post_author(request=request, data=request.data)
        return Response(data, status=code)


class AuthorView(APIView):
    permission_classes = (IsAuthenticatedThroughAuthService,)

    REQUESTER = AuthorRequester()

    def get(self, request, author_uuid):
        data, code = self.REQUESTER.get_author(request=request, uuid=author_uuid)
        return Response(data, status=code)

    def delete(self, request, author_uuid):
        data, code = self.REQUESTER.delete_author(request=request,uuid=author_uuid)
        return Response(data, status=code)

    def patch(self, request, author_uuid):
        data, code = self.REQUESTER.patch_author(request=request, uuid=author_uuid, data=request.data)
        return Response(data, status=code)


class AllBooksView(APIView):
    REQUESTER = BookRequester()

    def get (self, request):
        data, code = self.REQUESTER.get_all_books(request=request)
        return Response(data, status=code)

    def post(self, request):
        data, code = self.REQUESTER.post_book(request=request, data=request.data)
        print(request.data)
        return Response(data, status=code)


class BookView(APIView):
    permission_classes = (IsAuthenticatedThroughAuthService,)

    REQUESTER = BookRequester()

    def get(self, request, book_uuid):
        data, code = self.REQUESTER.get_book(request=request, uuid=book_uuid)
        return Response(data, status=code)

    def delete(self, request, book_uuid):
        data, code = self.REQUESTER.delete_book(request=request,uuid=book_uuid)
        return Response(data, status=code)

    def patch(self, request, book_uuid):
        data, code = self.REQUESTER.patch_book(request=request, uuid=book_uuid, data=request.data)
        print(request.data)
        return Response(data, status=code)


from django.shortcuts import redirect
from django.views import View
class OLoginView(View):
    def get(self, request):
        uri = 'http://127.0.0.1:8004/o/authorize/?' \
              'client_id=Gateway_id&' \
              'grant_type=authorization_code&' \
              'response_type=token'
        return redirect(uri)

class ORedirectView(APIView):
    def get(self, request: Request):
        import requests
        code = request.query_params['code']
        data_to_send = f'client_id=Gateway_id&client_secret=Gateway_secret&code={code}&grant_type=authorization_code'
        ret = requests.post(url='http://127.0.0.1:8004/o/token/', data=data_to_send,
                            headers={'content-type': 'application/x-www-form-urlencoded'})
        return Response(ret.json(), status=ret.status_code)