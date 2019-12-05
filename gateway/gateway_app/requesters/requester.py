import requests
import json
import re

class Requester:
	HOST = 'http://127.0.0.1'
	BASE_HTTP_ERROR = (json.dumps({'error': 'BaseHTTPError'}), 500)

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
			limit = request.query_params['limit']
			offset = request.query_params['offset']
		except KeyError:
			return None
		return limit, offset

	def get_data_from_response(self, response):
		try:
			return response.json()
		except (ValueError, json.JSONDecodeError, AttributeError):
			return response.text

	def find_limit_and_offset_in_link(self, link):
		limit_substr = re.findall(r'limit=\d+', link)
		offset_substr = re.findall(r'offset=\d+', link)
		limit = re.findall(r'\d+', limit_substr[0])
		offset = [0]
		if len(offset_substr) != 0:
			offset = re.findall(r'\d+', offset_substr[0])
		return limit[0], offset[0]

	def next_and_prev_links_to_params(self, data):
		try:
			next_link, prev_link = data['next'], data['previous']
		except (KeyError, TypeError):
			return data
		if next_link:
			limit, offset = self.find_limit_and_offset_in_link(next_link)
			data['next'] = f'?limit={limit}&offset={offset}'
		if prev_link:
			limit, offset = self.find_limit_and_offset_in_link(prev_link)
			data['previous'] = f'?limit={limit}&offset={offset}'
		return data

 