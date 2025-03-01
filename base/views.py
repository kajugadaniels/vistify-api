import requests
from base.models import *
from base.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categoryDetails(request, pk):
    """
    Retrieves detailed information for a specific Category identified by its primary key.
    Returns a comprehensive response with the category data or an error if not found.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            {
                "detail": f"Category with id {pk} not found. Please verify the provided identifier."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = CategorySerializer(category)
    return Response(
        {
            "detail": "Successfully retrieved category details.",
            "data": serializer.data
        },
        status=status.HTTP_200_OK
    )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editCategory(request, pk):
    """
    Updates an existing Category record with the provided data.
    Returns a detailed success message with updated category data or detailed error information if the update fails.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            {
                "detail": f"Category with id {pk} not found for update."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Category updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "detail": "Failed to update category. Please review the errors.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCategory(request, pk):
    """
    Deletes a specific Category record identified by its primary key.
    Returns a detailed confirmation message if deletion is successful, or an error if the category is not found.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            {
                "detail": f"Category with id {pk} not found. Deletion aborted."
            },
            status=status.HTTP_404_NOT_FOUND
        )
    category.delete()
    return Response(
        {
            "detail": f"Category with id {pk} has been deleted successfully."
        },
        status=status.HTTP_204_NO_CONTENT
    )

# --------------------------
# Tag CRUD Endpoints
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addTag(request):
    """
    Creates a new Tag record using the provided data.
    Returns a detailed success message with the created tag data or error details if creation fails.
    """
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "detail": "Tag created successfully.",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response_data = {
            "detail": "Failed to create tag. Please review the input data.",
            "errors": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tagDetails(request, pk):
    """
    Retrieves detailed information for a specific Tag identified by its primary key.
    Returns a detailed success message with the tag data or an error if not found.
    """
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        response_data = {
            "detail": f"Tag with id {pk} not found. Please verify the provided identifier."
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TagSerializer(tag)
    response_data = {
        "detail": "Successfully retrieved tag details.",
        "data": serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editTag(request, pk):
    """
    Updates an existing Tag record with the provided data.
    Returns a detailed success message with updated tag data or detailed error information if the update fails.
    """
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        response_data = {
            "detail": f"Tag with id {pk} not found for update."
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TagSerializer(tag, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "detail": "Tag updated successfully.",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "detail": "Failed to update tag. Please review the errors.",
            "errors": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTag(request, pk):
    """
    Deletes a specific Tag record identified by its primary key.
    Returns a detailed confirmation message if deletion is successful, or an error if the tag is not found.
    Note: We return a 200 OK status with a JSON body to ensure a Response object is always returned.
    """
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        response_data = {
            "detail": f"Tag with id {pk} not found. Deletion aborted."
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    tag.delete()
    response_data = {
        "detail": f"Tag with id {pk} has been deleted successfully."
    }
    return Response(response_data, status=status.HTTP_200_OK)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaceMenu(request, place_id):
    """
    Retrieve all menu items for a specific Place.
    """
    try:
        menu_items = PlaceMenu.objects.filter(place__id=place_id)
        serializer = PlaceMenuSerializer(menu_items, many=True)
        return Response(
            {
                "detail": f"Successfully retrieved {len(serializer.data)} menu items.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Place.DoesNotExist:
        return Response(
            {"detail": "Place not found."},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPlaceMenuItem(request, place_id):
    """
    Add a new food menu item to a specific Place.
    """
    data = request.data.copy()
    data['place'] = place_id
    serializer = PlaceMenuSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Menu item added successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "detail": "Failed to add menu item.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menuItemDetails(request, pk):
    """
    Retrieve details for a specific menu item.
    """
    try:
        menu_item = PlaceMenu.objects.get(pk=pk)
        serializer = PlaceMenuSerializer(menu_item)
        return Response(
            {
                "detail": "Successfully retrieved menu item details.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except PlaceMenu.DoesNotExist:
        return Response(
            {"detail": "Menu item not found."},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def editPlaceMenuItem(request, pk):
    """
    Update a menu item.
    """
    try:
        menu_item = PlaceMenu.objects.get(pk=pk)
    except PlaceMenu.DoesNotExist:
        return Response(
            {"detail": "Menu item not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PlaceMenuSerializer(menu_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "detail": "Menu item updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "detail": "Failed to update menu item.",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )