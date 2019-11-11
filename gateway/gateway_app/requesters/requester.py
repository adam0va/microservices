import requests
import json
import re

class Requester:
	HOST = 'http://127.0.0.1'
	BASE_HTTP_ERROR = (json.dumps({'error': 'Internal server error'}), 500)

	def get_request(self, url):
		try:
			response = requests.get(url)
		except requests.exceptions.BaseHTTPError:
			return None
		return response

	def post_request(self, url, data):
		try:
			response = requests.post(url=url, json=data)
		except requests.exceptions.BaseHTTPError:
			return None
		return response

	def patch_request(self, url, data):
		try:
			response = requests.patch(url=url, json=data)
		except requests.exceptions.BaseHTTPError:
			return None
		return response

	def delete_request(self, url):
		try:
			response = requests.delete(url=url)
		except requests.exceptions.BaseHTTPError:
			return None
		return response

	def get_limit_and_offset(self, request):
		try:
			limit = request.query_params('limit')
			offset = request.query_params('offset')
		except KeyError:
			return None
		return limit, offset

	def get_data_from_response(self, response):
		try:
			return response.json()
		except (ValueError, json.JSONDecodeError):
			return response.text

 