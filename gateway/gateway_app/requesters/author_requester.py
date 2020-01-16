from gateway_app.requesters.requester import Requester
from .author_queue import AuthorQueue


class AuthorRequester(Requester):
	author_queue = AuthorQueue()
	AUTHOR_HOST = Requester.HOST + ':8002/authors/'

	def get_all_authors(self, request):
		host = self.AUTHOR_HOST
		l_o = self.get_limit_and_offset(request)
		if l_o is not None:
			host += f'?limit={l_o[0]}&offset={l_o[1]}'
		response = self.get_request(host)
		if response is None:
			return self.BASE_HTTP_ERROR
		response_json = self.next_and_prev_links_to_params(self.get_data_from_response(response))
		AuthorRequester.author_queue.send_requests()
		return response_json, response.status_code

	def get_author(self, request, uuid):
		response = self.get_request(self.AUTHOR_HOST + f'{uuid}/')
		if response is None:
			return self.BASE_HTTP_ERROR
		AuthorRequester.author_queue.send_requests()
		return self.get_data_from_response(response), response.status_code

	def post_author(self, request, data):
		response = self.post_request(self.AUTHOR_HOST, data=data)
		if response is None:
			AuthorRequester.author_queue.add_post(data)
			return self.BASE_HTTP_ERROR
		AuthorRequester.author_queue.send_requests()
		return self.get_data_from_response(response), response.status_code

	def patch_author(self, request, uuid, data):
		response = self.patch_request(self.AUTHOR_HOST + f'{uuid}/', data=data)
		if response is None:
			AuthorRequester.author_queue.add_patch(uuid, data)
			return self.BASE_HTTP_ERROR
		AuthorRequester.author_queue.send_requests()
		return self.get_data_from_response(response), response.status_code

	def delete_author(self, request, uuid):
		from gateway_app.requesters.book_requester import BookRequester
		edited_books = BookRequester().erase_deleted_authors_uuid(uuid)

		response = self.delete_request(self.AUTHOR_HOST + f'{uuid}/')
		if response is None:
			AuthorRequester.author_queue.add_delete(uuid)
			BookRequester().return_deleted_authors_uuid(edited_books)
			return self.BASE_HTTP_ERROR
		if response.status_code != 204:
			BookRequester().return_deleted_authors_uuid(edited_books)
			return self.get_data_from_response(response), response.status_code
		AuthorRequester.author_queue.send_requests()
		return self.get_data_from_response(response), response.status_code
