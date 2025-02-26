import requests
from base.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([])  # This route is unprotected
def getRwandaLocations(request):
    """
    Retrieve Rwanda locations from the external RapidAPI endpoint and return the data.
    """
    url = "https://rwanda.p.rapidapi.com/"
    headers = {
        "x-rapidapi-key": "3107e210c4msh320bc0e06280efbp10cd72jsn0a5782a2d4b3"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return Response(
                {"detail": "Error fetching Rwanda locations."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse the API response
        api_data = response.json()
        serializer = RwandaLocationsSerializer(data=api_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the data does not match the expected schema, return the errors.
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaces(request):
    """
    Retrieve a list of all Places with nested images and social medias.
    """
    places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)