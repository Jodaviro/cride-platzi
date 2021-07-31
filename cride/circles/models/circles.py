"""Circle Model"""

#django
from django.db import models

#Utilities
from cride.utils.models import CRideModel

class Circle(CRideModel):
	"""Circle Model.

	A Circle is a prive gruop where rides are offered and talen
	by menbers. To join a circle   user must receive an unique
	invitation code from an existing circle member
	"""
	name = models.CharField(('circle name'), max_length=140)
	slug_name = models.SlugField(unique=True, max_length=40)
	about = models.CharField(('circle description'), max_length=255, blank=True)
	picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)
	members = models.ManyToManyField(
		'users.User',
		through='circles.Membership',
        through_fields=('circle', 'user')
	)

	# Stats
	rides_offered = models.PositiveIntegerField(default=0)
	rides_taken = models.PositiveIntegerField(default=0)
	is_verified = models.BooleanField(
		('verified circle'),
		default=False,
		help_text='Verified circles are also know as oficial comunities'
	)
	is_public = models.BooleanField(
		default=True,
		help_text='Public circles are listed in the main page so everybody know about their existense'
	)
	is_limited = models.BooleanField(
		('limited'),
		default=False,
		help_text='Limited circles can grow up to a fixed number of members'
	)
	members_limit = models.PositiveIntegerField(
		default=0,
		help_text='If circle is limited sets the member limit of the circle'
	)

	class Meta(CRideModel.Meta):
		"""Meta Class"""
		ordering = ['-rides_taken', '-rides_offered']

	def __str__(self):
		return self.name