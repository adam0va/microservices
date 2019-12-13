from django.test import TestCase
from readers_app.models import Reader
from rest_framework.test import APIClient
from django.test.runner import DiscoverRunner
import uuid

class ReadersListTestCase(TestCase):
	def setUp(self):		
		Reader.objects.create(name='Kate', surname='Frank', date_of_birth='1999-09-09')
		Reader.objects.create(name='Kat', surname='Franky', date_of_birth='1999-09-09')
		Reader.objects.create(name='Kata', surname='Franke', date_of_birth='1999-09-09')
		self.data_post_400 = {
			'name' : 'Ira',
		}
		self.data_post_201 = {
			'name' : 'Ira',
			'surname' : 'Adamova',
			'date_of_birth' : '1998-01-05',
		}

	def test_get_readers(self):
		client = APIClient()
		reader1 = Reader.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09')
		reader2 = Reader.objects.get(name='Kat', surname='Franky', date_of_birth='1999-09-09')
		reader3 = Reader.objects.get(name='Kata', surname='Franke', date_of_birth='1999-09-09')

		response = client.get('/readers/')
		self.assertEqual(len(response.data), 3)
		self.assertEqual(response.data[0]['uuid'], str(reader1.uuid))
		self.assertEqual(response.data[1]['uuid'], str(reader2.uuid))
		self.assertEqual(response.data[1]['name'], str(reader2.name))
		self.assertEqual(response.data[2]['name'], str(reader3.name))
		self.assertEqual(response.data[2]['surname'], str(reader3.surname))
		self.assertEqual(response.data[0]['surname'], str(reader1.surname))

	def test_post_reader400(self):
		client = APIClient()
		response = client.post('/readers/', data = self.data_post_400)
		self.assertEqual(response.status_code, 400)

	def test_post_reader201(self):
		client = APIClient()
		response = client.post('/readers/', data = self.data_post_201)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['name'], self.data_post_201['name'])
		self.assertEqual(response.data['surname'], self.data_post_201['surname'])
		self.assertEqual(response.data['date_of_birth'], self.data_post_201['date_of_birth'])

class ReaderDetailTestCase(TestCase):
	def setUp(self):		
		Reader.objects.create(name='Kate', surname='Frank', date_of_birth='1999-09-09')
		self.data_patch = {
			'name' : 'Lora',
			'surname' : 'Blue',
			'date_of_birth' :'1999-09-09',
		}
	def test_get_one_reader(self):
		client = APIClient()
		reader1 = Reader.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09')
		response = client.get('/readers/' + str(reader1.uuid) + '/')
		self.assertEqual(response.data['uuid'], str(reader1.uuid))
		self.assertEqual(response.data['name'], str(reader1.name))
		self.assertEqual(response.data['surname'], str(reader1.surname))
		self.assertEqual(response.data['date_of_birth'], str(reader1.date_of_birth))
	def test_get_one_reader404(self):
		client = APIClient()
		random_uuid = uuid.uuid4()
		response = client.get('/readers/' + str(random_uuid) + '/')
		self.assertEqual(response.status_code, 404)
	def test_patch_reader204(self):
		client = APIClient()
		reader1 = Reader.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09')
		response = client.patch('/readers/' + str(reader1.uuid) + '/', data = self.data_patch)
		self.assertEqual(response.status_code, 202)
	def test_delete_reader(self):
		client = APIClient()
		reader1 = Reader.objects.get(name='Kate', surname='Frank', date_of_birth='1999-09-09')
		response = client.delete('/readers/' + str(reader1.uuid) + '/')
		self.assertEqual(response.status_code, 204)
	
