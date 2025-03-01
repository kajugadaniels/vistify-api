from base.models import *
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

class PlaceMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceMenu
        fields = ['id', 'name', 'description', 'price']

class PlaceSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)
    images = PlaceImageSerializer(read_only=True, many=True)
    social_medias = PlaceSocialMediaSerializer(source='social_media', read_only=True)
    menu_items = PlaceMenuSerializer(many=True, read_only=True)  # ✅ FIXED: Removed `source` argument

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'category',
            'category_detail',
            'tags',
            'tags_detail',
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
            'menu_items',  # ✅ FIXED: Now correctly retrieving place menu
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']