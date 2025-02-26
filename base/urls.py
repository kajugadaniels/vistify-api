from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('rwanda-locations/', getRwandaLocations, name='getRwandaLocations'),

    path('places/', getPlaces, name='getPlaces'),
    path('places/add/', addPlace, name='addPlace'),
    path('places/<int:pk>/', placeDetails, name='placeDetails'),
    path('places/<int:pk>/edit/', editPlace, name='editPlace'),
    path('places/<int:pk>/delete/', deletePlace, name='deletePlace'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)