"""Circles Serializers"""


#Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#models 
from cride.circles.models import Circle


class CircleSerializer(serializers.Serializer):
	"""Circle Model Serializer"""
	name = serializers.CharField()
	slug_name = serializers.SlugField()
	about = serializers.CharField()
	rides_taken = serializers.IntegerField()
	rides_offered = serializers.IntegerField()
	members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
	"""Create Circle Model"""
	name = serializers.CharField(max_length=140)
	slug_name = serializers.SlugField(
		max_length=40,
		validators=[
			UniqueValidator(queryset=Circle.objects.all())
		]
	)
	about = serializers.CharField(max_length=255, required=False)
	picture = serializers.ImageField(required=False)

	def create(self, data):
		return Circle.objects.create(**data)

