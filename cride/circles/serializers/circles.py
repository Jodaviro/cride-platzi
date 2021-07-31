"""Circle Serializers"""

#Django REST Framework
from rest_framework import serializers

#models
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
	"""Circle Model Serializer"""

	class Meta:
		model = Circle
		fields = [
			'name',
		 	'slug_name',
		 	'about',
		 	'picture',
		 	'rides_taken',
		 	'is_verified',
		 	'is_limited',
		 	'is_public',
		]