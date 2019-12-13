from django.db import models
import uuid

class Book(models.Model):
	title = models.CharField(max_length=200)
	genre = models.CharField(max_length=200, blank=True)
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author_uuid = models.UUIDField(null=True, blank=True)
	reader_uuid = models.UUIDField(null=True, blank=True)
	def __str__(self):
 		return f'{self.title}, uuid: {self.uuid}'