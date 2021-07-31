"""Membership Model"""

#django
from django.db import models


#Utilities
from cride.utils.models import CRideModel

class Membership(CRideModel):
	"""Membership Models.
	
	A membership is the table that holds the relationship between
	a user and a circle.
	"""
	user = models.ForeignKey('users.User', on_delete=models.CASCADE)
	profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
	circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
	is_admin = models.BooleanField(
		('circle Admin'),
		default=False,
		help_text='Circle admin can update the  circles data and manage its members'
	)
	#Invitations
	used_invitations = models.PositiveSmallIntegerField(default=0)
	remaining_invitations = models.PositiveSmallIntegerField(default=0)
	invited_by = models.ForeignKey(
		'users.User',
		on_delete=models.SET_NULL,
		null=True,
		related_name='invited_by'
	)
	#Stats
	rides_taken = models.PositiveIntegerField(default=0)
	rides_offered = models.PositiveIntegerField(default=0)

	#Status
	is_active = models.BooleanField(
		('Active Status'),
		default=True,
		help_text='Only active users are allowed to interact in the circle'
	)

	def __str__(self):
		"""Return usename and circle"""
		return f'@{self.user.username}, {self.circle.slug_name}'

