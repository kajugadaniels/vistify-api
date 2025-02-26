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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlace(request):
    """
    Create a new Place with optional nested images and social medias.
    """
    serializer = PlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placeDetails(request, pk):
    """
    Retrieve detailed information for a specific Place.
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response({'detail': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlaceSerializer(place)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlace(request, pk):
    """
    Update an existing Place along with its nested images and social medias.
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response({'detail': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlaceSerializer(place, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlace(request, pk):
    """
    Delete a Place (along with its nested images and social medias).
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response({'detail': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)
    place.delete()
    return Response({'detail': 'Place deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaceImages(request, place_id):
    images = PlaceImage.objects.filter(place__id=place_id)
    serializer = PlaceImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlaceImage(request, place_id):
    data = request.data.copy()
    data['place'] = place_id
    serializer = PlaceImageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placeImageDetails(request, pk):
    try:
        image = PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
        return Response({"detail": "PlaceImage not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlaceImageSerializer(image)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlaceImage(request, pk):
    try:
        image = PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
        return Response({"detail": "PlaceImage not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlaceImageSerializer(image, data=request.data, partial=(request.method=='PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlaceImage(request, pk):
    try:
        image = PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
        return Response({"detail": "PlaceImage not found."}, status=status.HTTP_404_NOT_FOUND)
    image.delete()
    return Response({"detail": "PlaceImage deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaceSocialMedias(request, place_id):
    socials = PlaceSocialMedia.objects.filter(place__id=place_id)
    serializer = PlaceSocialMediaSerializer(socials, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlaceSocialMedia(request, place_id):
    data = request.data.copy()
    data['place'] = place_id
    serializer = PlaceSocialMediaSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placeSocialMediaDetails(request, pk):
    try:
        social = PlaceSocialMedia.objects.get(pk=pk)
    except PlaceSocialMedia.DoesNotExist:
        return Response({"detail": "PlaceSocialMedia not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlaceSocialMediaSerializer(social)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlaceSocialMedia(request, pk):
    try:
        social = PlaceSocialMedia.objects.get(pk=pk)
    except PlaceSocialMedia.DoesNotExist:
        return Response({"detail": "PlaceSocialMedia not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlaceSocialMediaSerializer(social, data=request.data, partial=(request.method=='PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlaceSocialMedia(request, pk):
    try:
        social = PlaceSocialMedia.objects.get(pk=pk)
    except PlaceSocialMedia.DoesNotExist:
        return Response({"detail": "PlaceSocialMedia not found."}, status=status.HTTP_404_NOT_FOUND)
    social.delete()
    return Response({"detail": "PlaceSocialMedia deleted successfully."}, status=status.HTTP_204_NO_CONTENT)