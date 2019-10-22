from rest_framework import serializers
from readers_app.models import Reader

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ['name', 'surname', 'date_of_birth', 'uuid']
    def create(self, validated_data):
    	new = Reader(**validated_data)
    	new.save()
    	return new