from django.test import TestCase
from authors_app.models import Author
from rest_framework.test import APIClient
from django.test.runner import DiscoverRunner
import uuid

class AuthorsListTestCase(TestCase):
	def setUp(self):		
		Author.objects.create(name='Kate', surname='Frank', date_of_birth='1999-09-09', country='Russia')
		Author.objects.create(name='Kat', surname='Franky', date_of_birth='1999-09-09', country='Russia')
		Author.objects.create(name='Kata', surname='Franke', date_of_birth='1999-09-09', country='Russia')
		self.data_post_400 = {
			'name' : 'Ira',
		}
		self.data_post_201 = {
			'name' : 'Ira',
			'surname' : 'Adamova',
			'date_of_birth' : '1998-01-05',
			'country' : 'Russia',
		}

	def test_get_authors(self):
		client = APIClient()
		author1 = Author.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09', country='Russia')
		author2 = Author.objects.get(name='Kat', surname='Franky', date_of_birth='1999-09-09', country='Russia')
		author3 = Author.objects.get(name='Kata', surname='Franke', date_of_birth='1999-09-09', country='Russia')

		response = client.get('/authors/')
		self.assertEqual(len(response.data), 3)
		self.assertEqual(response.data[0]['uuid'], str(author1.uuid))
		self.assertEqual(response.data[1]['uuid'], str(author2.uuid))
		self.assertEqual(response.data[1]['name'], str(author2.name))
		self.assertEqual(response.data[2]['name'], str(author3.name))
		self.assertEqual(response.data[2]['surname'], str(author3.surname))
		self.assertEqual(response.data[0]['surname'], str(author1.surname))

	def test_post_author400(self):
		client = APIClient()
		response = client.post('/authors/', data = self.data_post_400)
		self.assertEqual(response.status_code, 400)

	def test_post_author201(self):
		client = APIClient()
		response = client.post('/authors/', data = self.data_post_201)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['name'], self.data_post_201['name'])
		self.assertEqual(response.data['surname'], self.data_post_201['surname'])
		self.assertEqual(response.data['date_of_birth'], self.data_post_201['date_of_birth'])
		self.assertEqual(response.data['country'], self.data_post_201['country'])

class AuthorDetailTestCase(TestCase):
	def setUp(self):		
		Author.objects.create(name='Kate', surname='Frank', date_of_birth='1999-09-09', country='Russia')
		self.data_patch = {
			'name' : 'Lora',
			'surname' : 'Blue',
			'date_of_birth' :'1999-09-09', 
			'country' : 'Russia',
		}
	def test_get_one_author(self):
		client = APIClient()
		author1 = Author.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09', country='Russia')
		response = client.get('/authors/' + str(author1.uuid) + '/')
		self.assertEqual(response.data['uuid'], str(author1.uuid))
		self.assertEqual(response.data['name'], str(author1.name))
		self.assertEqual(response.data['surname'], str(author1.surname))
		self.assertEqual(response.data['date_of_birth'], str(author1.date_of_birth))
	def test_get_one_author404(self):
		client = APIClient()
		random_uuid = uuid.uuid4()
		response = client.get('/authors/' + str(random_uuid) + '/')
		self.assertEqual(response.status_code, 404)
	def test_patch_author204(self):
		client = APIClient()
		author1 = Author.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09', country='Russia')
		response = client.patch('/authors/' + str(author1.uuid) + '/', data = self.data_patch)
		self.assertEqual(response.status_code, 202)
	def test_delete_author(self):
		client = APIClient()
		author1 = Author.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09', country='Russia')
		response = client.delete('/authors/' + str(author1.uuid) + '/')
		self.assertEqual(response.status_code, 204)
	









