from rest_framework.views import Response, Request, APIView
from .requesters.book_requester import BookRequester
from .requesters.reader_requester import ReaderRequester
from .requesters.author_requester import AuthorRequester

class AllReadersView(APIView):
	REQUESTER = ReaderRequester()
	def get(self, request):
		data, code = self.REQUESTER.get_all_readers(request=request)
		return Response(data, status=code)

	def post(self, request):
		data, code = self.REQUESTER.post_reader(request=request, data=request.data)

class ReaderView(APIView):
	REQUESTER = ReaderRequester()
	def get(self, request, reader_uuid):
		data, code = self.REQUESTER.get_reader(request=request, uuid=reader_uuid)
		return Response(data, status=code)

	def delete(self, request, author_uuid):
		data, code = self.REQUESTER.delete_reader(request=request,uuid=author_uuid)
		return Response(data, status=code)

	def patch(self, request, author_uuid):
		data, code = self.REQUESTER.patch_reader(request=request, uuid=author_uuid, data=request.data)
		return Response(data, status=code)


class AllAuthorsView(APIView):
	REQUESTER = AuthorRequester()
	def get(self, request):
		data, code = self.REQUESTER.get_all_authors(request=request)
		return Response(data, status=code)

	def post(self, request):
		data, code = self.REQUESTER.post_author(request=request, data=request.data)

class AuthorView(APIView):
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

class BookView(APIView):
	REQUESTER = BookRequester()
	def get(self, request, book_uuid):
		data, code = self.REQUESTER.get_book(request=request, uuid=book_uuid)
		return Response(data, status=code)

	def delete(self, request, book_uuid):
		data, code = self.REQUESTER.delete_book(request=request,uuid=book_uuid)
		return Response(data, status=code)

	def patch(self, request, book_uuid):
		data, code = self.REQUESTER.patch_book(request=request, uuid=book_uuid, data=request.data)
		return Response(data, status=code)






