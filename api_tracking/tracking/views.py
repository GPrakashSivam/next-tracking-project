from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import TrackingNumber
from .serializers import TrackingNumberSerializer
import random
import string

class NextTrackingNumberView(APIView):
    def get(self, request, format=None):
       # Extract query parameters
        origin_country_id = request.query_params.get('origin_country_id', '')
        destination_country_id = request.query_params.get('destination_country_id', '')
        weight = request.query_params.get('weight', '')
        created_at = request.query_params.get('created_at', timezone.now().isoformat())
        customer_id = request.query_params.get('customer_id', '')
        customer_name = request.query_params.get('customer_name', '')
        customer_slug = request.query_params.get('customer_slug', '')

        # Validate required parameters
        #required_params = ['origin_country_id', 'destination_country_id', 'weight', 'created_at', 'customer_id', 'customer_name', 'customer_slug']
        #missing_params = [param for param in required_params if not request.query_params.get(param)]
        #if missing_params:
        #    raise ValidationError(f"Missing required parameters: {missing_params}")

        # Generate tracking number
        tracking_number = generate_tracking_number()
        while TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
            tracking_number = generate_tracking_number()

        # Create TrackingNumber instance
        tracking_number_data = {
            'tracking_number': tracking_number,
            'origin_country_id': origin_country_id,
            'destination_country_id': destination_country_id,
            'weight': weight,
            'created_at': created_at,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'customer_slug': customer_slug,
        }

        serializer = TrackingNumberSerializer(data=tracking_number_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Create a new dictionary with only the desired fields
        response_data = {
            'tracking_number': serializer.data['tracking_number'],
            'created_at': serializer.data['created_at'],
            'customer_slug': serializer.data['customer_slug'],
        }

        return Response(response_data)


def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))