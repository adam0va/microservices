from rest_framework import serializers
from authors_app.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'date_of_birth', 'country', 'uuid']
    def create(self, validated_data):
    	new = Author(**validated_data)
    	new.save()
    	return new