from django.db import models
import uuid

class Reader(models.Model):
	name = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)
	date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	def __str__(self):
 		return f'{self.name} {self.surname}, date of birth: {self.date_of_birth}, uuid: {self.uuid}'

# Create your models here.
