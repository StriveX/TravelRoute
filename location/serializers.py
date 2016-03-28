from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude', 'address', 'description', 'owner')

    def create(self, validated_data):
        name = validated_data.get('name', None)
        user = self.context.get('user')
        latitude = validated_data.get('latitude', None)
        longitude = validated_data.get('longitude', None)
        address = validated_data.get('address', None)
        description = validated_data.get('description', None)
        return Location.objects.create(name=name, owner=user, latitude=latitude, longitude=longitude, address=address, description=description)

