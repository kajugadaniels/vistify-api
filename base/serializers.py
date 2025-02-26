from rest_framework import serializers

class RwandaLocationsSerializer(serializers.Serializer):
    """
    Serializer for the Rwanda locations API response.
    Expected response structure:
      {
        "status": "success",
        "statusCode": 200,
        "message": "All provinces, districts, sectors, cells and villages from Rwanda",
        "data": [ ... ]
      }
    The 'data' field can contain a deeply nested structure so we use a JSONField.
    """
    status = serializers.CharField()
    statusCode = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField()
