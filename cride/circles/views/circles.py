"""Circles Views"""

#Django REST FRAMEWORK
from rest_framework import viewsets

#models
from cride.circles.models import Circle

#serializers
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
	"""Cicles ViewSet"""
	queryset = Circle.objects.all()
	serializer_class = CircleModelSerializer