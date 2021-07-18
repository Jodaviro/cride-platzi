"""Users Serializers"""

#Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

#Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

#Models
from cride.users.models import User, Profile


class UserModelSerializer(serializers.ModelSerializer):

	class Meta:
		"""User Serializer Meta Class"""
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'phone_number'
		)


class UserSignUpSerializer(serializers.Serializer):
	"""User SignUp Serializer.

	Handle sign up data validation and user/profile creation
	"""

	email = serializers.EmailField(
		validators=[
			UniqueValidator(queryset=User.objects.all())
		]
	)
	username = serializers.CharField(
		min_length = 4,
		max_length = 20,
		validators=[
			UniqueValidator(queryset=User.objects.all())
		]
	)
	phone_rexex = RegexValidator(
		regex=r'\+?1?\d{9,15}$',
		message='Phone number must entered be entered in format: +9999999999. Up to 15 digits allowed'
	)
	phone_number = serializers.CharField(
		max_length=17,
		validators=[phone_rexex]
	)
	
	#Password
	password = serializers.CharField(min_length=8, max_length=64)
	password_confirm = serializers.CharField(min_length=8, max_length=64)
	
	#Name
	first_name = serializers.CharField(min_length=2, max_length=30)
	last_name = serializers.CharField(min_length=2, max_length=30)

	def validate(self, data):
		"""Verify password match"""
		password = data['password']
		password_confirm = data['password_confirm']
		if password != password_confirm:
			raise serializers.ValidationError("passwords don't match")
		password_validation.validate_password(password)
		return data

	def create(self, data):
		"""Handle User and Profile Creation.
		"""
		data.pop('password_confirm')
		user = User.objects.create_user(**data)	
		profile = Profile.objects.create(user=user)
		return user


class UserLoginSerializer(serializers.Serializer):
	"""User Login Serializer.
	Handle the login request data.
	"""
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		"""Verifies credentials"""
		user = authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Invalid Credentials')
		self.context['user'] = user
		return data

	def create(self, data):
		"""Geneate or retrieve a new token."""
		token, created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key


