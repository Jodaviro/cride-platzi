"""Django Models utils."""

#Django
from django.db import models

class CRideModel(models.Model):
	"""Comparte Ride base Model
	CRide Model acts as an abstract base clase for every model in the projects.
	This class provide created and modified fields for every model.
	"""
	created = models.DateTimeField(
		'created at',
		auto_now_add=True,
		help_text='Date time on wich the objects was created'
	)
	modified = models.DateTimeField(
		'modified at',
		auto_now=True,
		help_text='Date time on wich the objects was last modified'
	)

	class Meta:
		"""Meta options"""
		abstract = True
		get_latest_by = 'created'
		ordering = ['-created', '-modifed']
