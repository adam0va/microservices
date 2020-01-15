from rest_framework import serializers
from books_app.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'uuid', 'author_uuid', 'reader_uuid']

    def create(self, validated_data):
    	new = Book(**validated_data)
    	new.save()
    	return new