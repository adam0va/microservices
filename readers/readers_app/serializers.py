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

    def extra_attr(self):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
        print(unknown_keys)
        return unknown_keys != set()