""" Circle Views """

#Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer


#models
from cride.circles.models import Circle

@api_view(['GET'])
def list_circles(request):
	"""Lists Circles"""
	circles = Circle.objects.filter(is_public=True)
	serializers = CircleSerializer(circles, many=True)
	return Response(serializers.data)

@api_view(['POST'])
def create_circle(request):
	"""Creates a new circle."""
	serializer =  CreateCircleSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	circle = serializer.save()
	return Response(CreateCircleSerializer(circle).data)
