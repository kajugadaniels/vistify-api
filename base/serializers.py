from base.models import Category, Tag, Place, PlaceImage, PlaceSocialMedia
from rest_framework import serializers

class RwandaLocationsSerializer(serializers.Serializer):
    """
    Serializer for the Rwanda locations API response.
    Expected structure:
      {
          "status": "success",
          "statusCode": 200,
          "message": "All provinces, districts, sectors, cells and villages from Rwanda",
          "data": [ ... ]
      }
    """
    status = serializers.CharField()
    statusCode = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

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

# Updated Place serializer with nested detailed information
class PlaceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    images = PlaceImageSerializer(read_only=True, many=True)
    social_medias = PlaceSocialMediaSerializer(read_only=True, many=True)
    
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
            'updated_at',
            'images',
            'social_medias',
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']
