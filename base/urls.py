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
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)