"""Users Models"""

#django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

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
	is_staff = models.BooleanField(
		('staff status'),
		default=False,
		help_text=('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		('active'),
		default=True,
		help_text=(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
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
	first_name = models.CharField(('first name'), max_length=150, blank=True)
	last_name = models.CharField(('last name'), max_length=150, blank=True)
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

	# objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

	class Meta:
		verbose_name = ('user')
		verbose_name_plural = ('users')


	def get_full_name(self):
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.username

	def __str__(self):
		return self.username