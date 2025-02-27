import requests
from base.models import *
from base.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# --------------------------
# External API: Rwanda Locations
# --------------------------
@api_view(['GET'])
@permission_classes([])  # Unprotected route
def getRwandaLocations(request):
    """
    Fetches Rwanda locations from the external RapidAPI endpoint and returns a detailed response.
    """
    url = "https://rwanda.p.rapidapi.com/"
    headers = {
        "x-rapidapi-key": "3107e210c4msh320bc0e06280efbp10cd72jsn0a5782a2d4b3"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            # Return a detailed error if the external API call fails
            return Response(
                {
                    "detail": f"Error fetching Rwanda locations. External API returned status code {response.status_code}."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse and validate the external API response
        api_data = response.json()
        serializer = RwandaLocationsSerializer(data=api_data)
        if serializer.is_valid():
            return Response(
                {
                    "detail": "Successfully retrieved Rwanda locations.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            # Provide detailed serializer error feedback
            return Response(
                {
                    "detail": "Data validation error from external API response.",
                    "errors": serializer.errors
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except Exception as e:
        # Catch and return any unexpected errors
        return Response(
            {
                "detail": "An unexpected error occurred while fetching Rwanda locations.",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )