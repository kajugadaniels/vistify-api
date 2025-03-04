from web.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'web'

urlpatterns = [
    path('rwanda-locations/', getRwandaLocations, name='getRwandaLocations'),

    path('categories/', getCategories, name='getCategories'),
    
    path('tags/', getTags, name='getTags'),

    path('places/', getPlaces, name='getPlaces'),
    path('place/<int:pk>/', placeDetails, name='placeDetails'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)