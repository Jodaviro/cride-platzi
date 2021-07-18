"""Users Models"""

#django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator

#Utilities
from cride.utils.models import CRideModel

class User(CRideModel, AbstractUser):
	"""
	Custom User Model. 
	Extends from django AbstractBaseUser, change the username field
	to email field and add some extra fields.
	"""
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
		error_messages={
			'unique':("A user with that email already exists."),
		},
	)
	is_client = models.BooleanField(
		('client status'),
		default=True,
		help_text=(
			'Designates whether the user is client.' 
			'Helps easily distinguish user and perform queries'
			'Clients are the main type of user'
		),
	)
	is_verified = models.BooleanField(
		('veridied client'),
		default=False,
		help_text=(
			'Set to True when the user have verified its email'
		),
	)
	phone_rexex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message='Phone number must entered be entered in format: +9999999999. Up to 15 digits allowed'
	)
	phone_number = models.CharField(
		('phone number'),
		max_length=17,
		blank=True,
		validators=[phone_rexex],
	)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.username

	def __str__(self):
		return self.username