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

class PlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializer(many=True, required=False)
    socialMedias = PlaceSocialMediaSerializer(source='social_medias', many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
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
            'updated_at',
            'images',
            'socialMedias'
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        social_medias_data = validated_data.pop('social_medias', [])
        place = Place.objects.create(**validated_data)
        # Create nested PlaceImage objects
        for image_data in images_data:
            PlaceImage.objects.create(place=place, **image_data)
        # Create nested PlaceSocialMedia objects
        for social_data in social_medias_data:
            PlaceSocialMedia.objects.create(place=place, **social_data)
        return place

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        social_medias_data = validated_data.pop('social_medias', None)
        
        # Update main Place fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle nested PlaceImage updates:
        if images_data is not None:
            # Clear existing images and re-create them (simplest approach)
            instance.images.all().delete()
            for image_data in images_data:
                PlaceImage.objects.create(place=instance, **image_data)

        # Handle nested PlaceSocialMedia updates:
        if social_medias_data is not None:
            instance.social_medias.all().delete()
            for social_data in social_medias_data:
                PlaceSocialMedia.objects.create(place=instance, **social_data)

        return instance