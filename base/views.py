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

# --------------------------
# Category CRUD Endpoints
# --------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCategory(request):
    """
    Creates a new Category record using the provided data.
    Returns a detailed success message with the created category data or error details if creation fails.
    """
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Category created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "detail": "Failed to create category. Please review the input data.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

# --------------------------
# Place CRUD Endpoints
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlace(request):
    """
    Creates a new Place using provided data.
    """
    serializer = PlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Place created successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "detail": "Failed to create Place. Please review the errors.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placeDetails(request, pk):
    """
    Retrieves detailed information for a specific Place along with its nested 
    category, tags, images, and social media records.
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
    serializer = PlaceSerializer(place)
    return Response(
        {
            "detail": "Successfully retrieved comprehensive details for the selected Place.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlace(request, pk):
    """
    Updates an existing Place record with the provided data.
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response(
            {
                "detail": f"Place with id {pk} not found for update."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = PlaceSerializer(place, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Place updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "detail": "Failed to update Place. Please review the provided data.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlace(request, pk):
    """
    Deletes a specific Place record.
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response(
            {
                "detail": f"Place with id {pk} not found. Deletion aborted."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    place.delete()
    return Response(
        {
            "detail": f"Place with id {pk} has been deleted successfully."
        },
        status=status.HTTP_204_NO_CONTENT
    )

# --------------------------
# PlaceImage CRUD Endpoints
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaceImages(request, place_id):
    """
    Retrieves all images for a given Place.
    """
    images = PlaceImage.objects.filter(place__id=place_id).order_by('-id')
    serializer = PlaceImageSerializer(images, many=True)
    return Response(
        {
            "detail": f"Successfully retrieved {len(serializer.data)} images for Place id {place_id}.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlaceImage(request, place_id):
    """
    Adds a new image to a specified Place.
    """
    data = request.data.copy()
    data['place'] = place_id
    serializer = PlaceImageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Place image added successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "detail": "Failed to add place image. Please check the input data.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placeImageDetails(request, pk):
    """
    Retrieves detailed information for a specific PlaceImage.
    """
    try:
        image = PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
        return Response(
            {
                "detail": f"PlaceImage with id {pk} not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = PlaceImageSerializer(image)
    return Response(
        {
            "detail": "Successfully retrieved place image details.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlaceImage(request, pk):
    """
    Updates an existing PlaceImage with new data.
    """
    try:
        image = PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
        return Response(
            {
                "detail": f"PlaceImage with id {pk} not found for update."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = PlaceImageSerializer(image, data=request.data, partial=(request.method=='PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Place image updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "detail": "Failed to update place image. Review the errors for more details.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlaceImage(request, pk):
    """
    Deletes a specific PlaceImage.
    """
    try:
        image = PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
        return Response(
            {
                "detail": f"PlaceImage with id {pk} not found. Deletion aborted."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    image.delete()
    return Response(
        {
            "detail": f"PlaceImage with id {pk} has been deleted successfully."
        },
        status=status.HTTP_204_NO_CONTENT
    )

# --------------------------
# PlaceSocialMedia CRUD Endpoints
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaceSocialMedias(request, place_id):
    """
    Retrieves all social media links associated with a given Place.
    """
    socials = PlaceSocialMedia.objects.filter(place__id=place_id).order_by('-id')
    serializer = PlaceSocialMediaSerializer(socials, many=True)
    return Response(
        {
            "detail": f"Successfully retrieved {len(serializer.data)} social media records for Place id {place_id}.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlaceSocialMedia(request, place_id):
    """
    Adds a new social media record for a specified Place.
    """
    data = request.data.copy()
    data['place'] = place_id
    serializer = PlaceSocialMediaSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Place social media record added successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "detail": "Failed to add social media record. Check the submitted data.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placeSocialMediaDetails(request, pk):
    """
    Retrieves detailed information for a specific PlaceSocialMedia record.
    """
    try:
        social = PlaceSocialMedia.objects.get(pk=pk)
    except PlaceSocialMedia.DoesNotExist:
        return Response(
            {
                "detail": f"PlaceSocialMedia with id {pk} not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = PlaceSocialMediaSerializer(social)
    return Response(
        {
            "detail": "Successfully retrieved social media details.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlaceSocialMedia(request, pk):
    """
    Updates an existing PlaceSocialMedia record.
    """
    try:
        social = PlaceSocialMedia.objects.get(pk=pk)
    except PlaceSocialMedia.DoesNotExist:
        return Response(
            {
                "detail": f"PlaceSocialMedia with id {pk} not found for update."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = PlaceSocialMediaSerializer(social, data=request.data, partial=(request.method=='PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Social media record updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "detail": "Failed to update social media record. Please review the errors.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlaceSocialMedia(request, pk):
    """
    Deletes a specific PlaceSocialMedia record.
    """
    try:
        social = PlaceSocialMedia.objects.get(pk=pk)
    except PlaceSocialMedia.DoesNotExist:
        return Response(
            {
                "detail": f"PlaceSocialMedia with id {pk} not found. Deletion aborted."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    social.delete()
    return Response(
        {
            "detail": f"PlaceSocialMedia with id {pk} has been deleted successfully."
        },
        status=status.HTTP_204_NO_CONTENT
    )
