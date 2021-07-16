"""Profile model"""

#django
from django.db import models
#utilities
from cride.utils.models import CRideModel

class Profile(CRideModel):
	"""
	Profile Model extension from Users
	Holds user's public datta like biography, picture, and statistics
	"""
	user = models.OneToOneField('users.User', on_delete=models.CASCADE, primary_key=True)
	picture = models.ImageField(
		('profile picture'),
		upload_to='users/pictures',
		blank=True,
		null=True
	)
	biography = models.TextField(max_length=500, blank=True)

	# Stats
	rides_taken = models.PositiveIntegerField(default=0)
	rides_offered = models.PositiveIntegerField(default=0)
	reputation = models.FloatField(
		default=5.0,
		help_text='Users reputation base on the rides taken and offered.'
	)

	def __str__(self):
		return self.user.username