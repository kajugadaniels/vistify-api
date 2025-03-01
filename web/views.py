import requests
from base.models import *
from base.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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

@api_view(['GET'])
@permission_classes([AllowAny])
def getCategories(request):
    """
    Retrieves all Category records, ordered by newest first.
    Returns a detailed response with the number of categories retrieved.
    """
    categories = Category.objects.all().order_by('-id')
    serializer = CategorySerializer(categories, many=True)
    return Response(
        {
            "detail": f"Successfully retrieved {len(serializer.data)} categories.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def getTags(request):
    """
    Retrieves all Tag records, ordered by newest first.
    Returns a detailed response with the count of tags retrieved.
    """
    tags = Tag.objects.all().order_by('-id')
    serializer = TagSerializer(tags, many=True)
    response_data = {
        "detail": f"Successfully retrieved {len(serializer.data)} tags.",
        "data": serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getPlaces(request):
    """
    Retrieves all Place records with detailed information for category, tags,
    place images, and social media records.
    """
    places = Place.objects.all().order_by('-id')
    serializer = PlaceSerializer(places, many=True)
    return Response(
        {
            "detail": f"Successfully retrieved {len(serializer.data)} places with detailed info.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def placeDetails(request, pk):
    """
    Retrieves detailed information for a specific Place, including:
    - Category
    - Tags
    - Images
    - Social Media
    - Menu Items (Food & Drinks)
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response(
            {
                "detail": f"Place with id {pk} not found. Please verify the provided identifier."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # Serialize place details
    place_serializer = PlaceSerializer(place)

    # Retrieve place's menu
    menu_items = PlaceMenu.objects.filter(place=place).order_by('name')
    menu_serializer = PlaceMenuSerializer(menu_items, many=True)

    return Response(
        {
            "detail": "Successfully retrieved comprehensive details for the selected Place.",
            "data": {
                "place": place_serializer.data,
                "menu": menu_serializer.data  # ✅ Now retrieving place menu items
            }
        },
        status=status.HTTP_200_OK
    )