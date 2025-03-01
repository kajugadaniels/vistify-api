from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
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

    path('categories/', getCategories, name='getCategories'),
    path('category/add/', addCategory, name='addCategory'),
    path('category/<int:pk>/', categoryDetails, name='categoryDetails'),
    path('category/<int:pk>/edit/', editCategory, name='editCategory'),
    path('category/<int:pk>/delete/', deleteCategory, name='deleteCategory'),
    
    path('tags/', getTags, name='getTags'),
    path('tag/add/', addTag, name='addTag'),
    path('tag/<int:pk>/', tagDetails, name='tagDetails'),
    path('tag/<int:pk>/edit/', editTag, name='editTag'),
    path('tag/<int:pk>/delete/', deleteTag, name='deleteTag'),

    path('place/<int:place_id>/menu/', getPlaceMenu, name='getPlaceMenu'),
    path('place/<int:place_id>/menu/add/', addPlaceMenuItem, name='addPlaceMenuItem'),
    path('menu/<int:pk>/', menuItemDetails, name='menuItemDetails'),
    path('menu/<int:pk>/edit/', editPlaceMenuItem, name='editPlaceMenuItem'),
    path('menu/<int:pk>/delete/', deletePlaceMenuItem, name='deletePlaceMenuItem'),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)