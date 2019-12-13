from django.test import TestCase
from books_app.models import Book
from rest_framework.test import APIClient
from django.test.runner import DiscoverRunner
import uuid

class BooksListTestCase(TestCase):
	def setUp(self):		
		Book.objects.create(title='Cat', author_uuid=uuid.uuid4(), reader_uuid=uuid.uuid4())
		Book.objects.create(title='Dog', author_uuid=uuid.uuid4(), reader_uuid=uuid.uuid4())
		Book.objects.create(title='Mouse', author_uuid=uuid.uuid4(), reader_uuid=uuid.uuid4())
		self.random_uuid_author = uuid.uuid4()
		self.data_post_400 = {
			'tit' : 'cat',
		}
		self.data_post_201 = {
			'title' : 'Cow',
			'author_uuid' : self.random_uuid_author,
		}

	def test_get_books(self):
		client = APIClient()
		book1 = Book.objects.get(title='Cat')
		book2 = Book.objects.get(title='Dog')
		book3 = Book.objects.get(title='Mouse')

		response = client.get('/books/')
		self.assertEqual(len(response.data), 3)
		self.assertEqual(response.data[0]['uuid'], str(book1.uuid))
		self.assertEqual(response.data[0]['title'], str(book1.title))
		self.assertEqual(response.data[1]['author_uuid'], str(book2.author_uuid))
		self.assertEqual(response.data[1]['reader_uuid'], str(book2.reader_uuid))
		self.assertEqual(response.data[2]['title'], str(book3.title))
		self.assertEqual(response.data[2]['uuid'], str(book3.uuid))

	def test_post_book400(self):
		client = APIClient()
		response = client.post('/books/', data = self.data_post_400)
		self.assertEqual(response.status_code, 400)

	def test_post_book201(self):
		client = APIClient()
		response = client.post('/books/', data = self.data_post_201)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['title'], self.data_post_201['title'])
		self.assertEqual(response.data['author_uuid'], str(self.random_uuid_author))

class BookDetailTestCase(TestCase):
	def setUp(self):		
		Book.objects.create(title='Cat', author_uuid=uuid.uuid4(), reader_uuid=uuid.uuid4())
		self.random_uuid_reader = uuid.uuid4()
		self.data_patch = {
			'title' : 'Cow',
			'author_uuid' : self.random_uuid_reader,
		}
	def test_get_one_book(self):
		client = APIClient()
		book1 = Book.objects.get(title='Cat')
		response = client.get('/books/' + str(book1.uuid) + '/')
		self.assertEqual(response.data['uuid'], str(book1.uuid))
		self.assertEqual(response.data['title'], str(book1.title))
		self.assertEqual(response.data['author_uuid'], str(book1.author_uuid))
		self.assertEqual(response.data['reader_uuid'], str(book1.reader_uuid))
	def test_get_one_book404(self):
		client = APIClient()
		random_uuid = uuid.uuid4()
		response = client.get('/books/' + str(random_uuid) + '/')
		self.assertEqual(response.status_code, 404)
	def test_patch_book204(self):
		client = APIClient()
		book1 = Book.objects.get(title='Cat')
		response = client.patch('/books/' + str(book1.uuid) + '/', data = self.data_patch)
		self.assertEqual(response.status_code, 202)
	def test_delete_book(self):
		client = APIClient()
		book1 = Book.objects.get(title='Cat')
		response = client.delete('/books/' + str(book1.uuid) + '/')
		self.assertEqual(response.status_code, 204)
