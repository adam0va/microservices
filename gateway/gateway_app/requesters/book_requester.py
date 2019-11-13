from gateway_app.requesters.requester import Requester

class BookRequester(Requester):
	BOOK_HOST = Requester.HOST + ':8003/books/'

	def set_author(self, request, book):
		from gateway_app.requesters.author_requester import AuthorRequester
		author_id = book['author_uuid']
		if author_id is not None:
			author_json, author_status = AuthorRequester().get_author(request=request, uuid=author_id)
			book['author'] = author_json
			return book, author_status
		else:
			return book, 200

	def set_reader(self, request, book):
		from gateway_app.requesters.reader_requester import ReaderRequester
		reader_id = book['reader_uuid']
		if reader_id is not None:
			reader_json, reader_status = ReaderRequester().get_reader(request=request, uuid=reader_id)
			book['reader'] = reader_json
			return book, reader_status
		else:
			return book, 200

	def author_excists(self, request, data):
		from gateway_app.requesters.author_requester import AuthorRequester
		if data['author_uuid']:
			_, code = AuthorRequester().get_author(request, data['author_uuid'])
			return code == 200
		return {}, 200

	def reader_excists(self, request, data):
		from gateway_app.requesters.reader_requester import ReaderRequester
		if data['reader_uuid']:
			_, code = ReaderRequester().get_reader(request, data['reader_uuid'])
			return code == 200
		return {}, 200
	#-------------------------------------------------------------------------------------------

	def get_all_books(self, request):
		host = self.BOOK_HOST

		response = self.get_request(host)
		if response is None:
			return self.BASE_HTTP_ERROR

		response_data = response.json()
		print('response')
		print(response_data)
		print('----')
		print(response_data[0])

		for i in range(len(response_data)):
			response_data[i], status_code = self.set_reader(request, response_data[i])
			if status_code != 200:
				return response_data, response.status_code
			response_data[i], status_code = self.set_author(request, response_data[i])
			if status_code != 200:
				return response_data, response.status_code
		return response_data, status_code

	def get_book(self, request, uuid):
		response = self.get_request(self.BOOK_HOST + uuid + '/')
		if response is None:
			return self.BASE_HTTP_ERROR
		if response.status_code != 200:
			return response, response.status_code

		response_data = response.json()
		try:
			response_data, status_code = self.set_reader(request, response_data)
			if status_code != 200:
				return response_data, status_code
		except KeyError:
			return {'error': 'No reader uuid was given'}, 500
		try:
			response_data, status_code = self.set_author(request, response_data)
			if status_code != 200:
				return response_data, status_code
		except KeyError:
			return {'error': 'No author uuid was given'}, 500
		return response_data, 200

	def delete_book(self, request, uuid):
		response = self.delete_request(self.BOOK_HOST + uuid + '/')
		if response is None:
			return self.BASE_HTTP_ERROR
		return response, response.status_code
	
	def patch_book(self, request, uuid, data):
		#проверить есть ли такой читатель
		if not self.reader_excists(request, data):
			return {'error' : 'Wrong reader uuid'}, 404
		#проверить есть ли такой автор
		if not self.author_excists(request, data):
			return {'error' : 'Wrong author uuid'}, 404
		#поменять информацию
		response = self.patch_request(self.BOOK_HOST + uuid + '/', data=data)
		if response is None:
			return self.BASE_HTTP_ERROR
		return response.json(), response.status_code

	










