from rest_framework import serializers
from .models import Listing, ListingPhoto


class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingPhoto
        fields = ['id', 'image', 'order', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    photos = ListingPhotoSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'user', 'author_name', 'listing_type', 'property_type',
            'city', 'district', 'address', 'latitude', 'longitude',
            'budget_min', 'budget_max', 'description',
            'is_active', 'photos', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ListingDetailSerializer(ListingSerializer):
    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields
