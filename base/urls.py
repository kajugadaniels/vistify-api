from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('rwanda-locations/', getRwandaLocations, name='getRwandaLocations'),

    path('places/', getPlaces, name='getPlaces'),
    path('place/add/', addPlace, name='addPlace'),
    path('place/<int:pk>/', placeDetails, name='placeDetails'),
    path('place/<int:pk>/edit/', editPlace, name='editPlace'),
    path('place/<int:pk>/delete/', deletePlace, name='deletePlace'),

    path('place/<int:place_id>/images/', getPlaceImages, name='getPlaceImages'),
    path('place/<int:place_id>/images/add/', addPlaceImage, name='addPlaceImage'),
    path('images/<int:pk>/', placeImageDetails, name='placeImageDetails'),
    path('images/<int:pk>/edit/', editPlaceImage, name='editPlaceImage'),
    path('images/<int:pk>/delete/', deletePlaceImage, name='deletePlace_Image'),

    path('places/<int:place_id>/social/', getPlaceSocialMedias, name='getPlaceSocialMedias'),
    path('places/<int:place_id>/social/add/', addPlaceSocialMedia, name='addPlaceSocialMedia'),
    path('social/<int:pk>/', placeSocialMediaDetails, name='placeSocialMediaDetails'),
    path('social/<int:pk>/edit/', editPlaceSocialMedia, name='editPlaceSocialMedia'),
    path('social/<int:pk>/delete/', deletePlaceSocialMedia, name='deletePlaceSocialMedia'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)