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
		if 'author_uuid' in data:
			_, code = AuthorRequester().get_author(request, data['author_uuid'])
			return code == 200 or data['author_uuid'] == None
		return 200

	def reader_excists(self, request, data):
		from gateway_app.requesters.reader_requester import ReaderRequester
		if 'reader_uuid' in data:
			_, code = ReaderRequester().get_reader(request, data['reader_uuid'])
			return code == 200 or data['reader_uuid'] == None
		return 200

	def erase_uuid(self, book, whos, uuid):
		if whos == 'author':
			if book['author_uuid'] == uuid:
				book['author_uuid'] = None
				response = self.patch_request(self.BOOK_HOST + book['uuid'] + '/', data=book)
				return response, response.status_code

		elif whos == 'reader':
			if book['reader_uuid'] == uuid:
				book['reader_uuid'] = None
				response = self.patch_request(self.BOOK_HOST + book['uuid'] + '/', data=book)
				return response, response.status_code
		return {}, 200

	def erase_deleted_authors_uuid(self, uuid):
		response = self.get_request(self.BOOK_HOST)
		if response is None:
			print(1)
			print(response)
			return self.BASE_HTTP_ERROR
		response_data = self.get_data_from_response(response)
		for i in range(len(response_data)):
			response, status = self.erase_uuid(response_data[i], 'author', uuid)
		return response, status

	def erase_deleted_readers_uuid(self, uuid):
		response = self.get_request(self.BOOK_HOST)
		if response is None:
			return response
		response_data = self.get_data_from_response(response)
		for i in range(len(response_data)):
			response, status = self.erase_uuid(response_data[i], 'reader', uuid)
		return response, status

	#-------------------------------------------------------------------------------------------

	def get_all_books(self, request):
		
		host = self.BOOK_HOST

		response = self.get_request(host)
		l_o = self.get_limit_and_offset(request)
		if l_o is not None:
			host += f'?limit={l_o[0]}&offset={l_o[1]}'
		print(f'host: {host}')
		response = self.get_request(host)
		if response is None:
			return self.BASE_HTTP_ERROR
		response_data = self.next_and_prev_links_to_params(self.get_data_from_response(response))

		if isinstance(response_data, dict):
			actual_messages = response_data['results']
			for i in range(len(actual_messages)):
				actual_messages[i], status_code = self.set_reader(request, actual_messages[i])
				if status_code != 200:
					return actual_messages, response.status_code
				actual_messages[i], status_code = self.set_author(request, actual_messages[i])
				if status_code != 200:
					return actual_messages, response.status_code
			response_data['results'] = actual_messages
		else:
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
		return self.get_data_from_response(response), response.status_code
	
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
		return self.get_data_from_response(response), response.status_code

	def post_book(self, request, data):
		if not self.reader_excists(request, data):
			return {'error' : 'Wrong reader uuid'}, 400
		if not self.author_excists(request, data):
			return {'error' : 'Wrong author uuid'}, 400

		response = self.post_request(self.BOOK_HOST, data=data)
		if response is None:
			return Requester.BASE_HTTP_ERROR
		
		return self.get_data_from_response(response), response.status_code



	










