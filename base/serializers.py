from base.models import *
from rest_framework import serializers

class RwandaLocationsSerializer(serializers.Serializer):
    """
    Serializer for the Rwanda locations API response.
    Expected response structure:
        {
            "status": "success",
            "statusCode": 200,
            "message": "All provinces, districts, sectors, cells and villages from Rwanda",
            "data": [ ... ]
        }
    The 'data' field can contain a deeply nested structure so we use a JSONField.
    """
    status = serializers.CharField()
    statusCode = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField()

class PlaceSerializer(serializers.ModelSerializer):
    # Use primary key representation for related fields.
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        allow_null=True, 
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), 
        many=True, 
        required=False
    )
    
    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'category',
            'tags',
            'province',
            'district',
            'sector',
            'cell',
            'village',
            'address',
            'latitude',
            'longitude',
            'views',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']

class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'place', 'image', 'caption', 'created_at']
        read_only_fields = ['id', 'created_at']

class PlaceSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceSocialMedia
        fields = [
            'id',
            'place',
            'phone_number',
            'email',
            'instagram',
            'tiktok',
            'twitter',
            'website',
            'facebook',
            'whatsapp'
        ]
        read_only_fields = ['id']