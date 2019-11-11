from gateway_app.requesters.requester import Requester

class ReaderRequester(Requester):
	READER_HOST = Requester.HOST + ':8001/readers/'

	def get_all_readers(self, request):
		response = self.get_request(self.READER_HOST)
		if response is None:
			return self.BASE_HTTP_ERROR
		return self.get_data_from_response(response), response.status_code

	def get_reader(self, request, uuid):
		response = self.get_request(self.READER_HOST + f'{uuid}/')
		if response is None:
			return self.BASE_HTTP_ERROR
		return self.get_data_from_response(response), response.status_code

	def post_reader(self, request, data):
		response = self.post_request(self.READER_HOST, data=data)
		if response is None:
			return self.BASE_HTTP_ERROR
		return self.get_data_from_response(response), response.status_code

	def patch_reader(self, request, uuid, data):
		response = self.patch_request(self.READER_HOST + f'{uuid}/', data=data)
		if response is None:
			return self.BASE_HTTP_ERROR
		return self.get_data_from_response(response), response.status_code

	def delete_reader(self, request, uuid):
		response = self.delete_request(self.READER_HOST + f'{uuid}/')
		if response is None:
			return self.BASE_HTTP_ERROR
		return self.get_data_from_response(response), response.status_code