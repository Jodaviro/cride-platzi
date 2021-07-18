"""Users Serializers"""

#Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings


#Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

#Models
from cride.users.models import User, Profile

#Utilities
from datetime import timedelta
import jwt


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
		user = User.objects.create_user(**data, is_verified=False)	
		Profile.objects.create(user=user)
		self.send_confirmation_email(user)
		return user

	def send_confirmation_email(self, user):
		"""Send confirmation mail link for account activation"""
		verification_token = self.gen_verification_token(user)
		subject = 'Welcome @{user.username}!. Please verify your account'
		from_email = 'Comparte Ride <noreply@comparteride.com>'
		content = render_to_string(
			'emails/users/account_verification.html',
			context={
				'token': verification_token,
				'user': user
			}
		)
		msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
		msg.attach_alternative(content, "text/html")
		msg.send()

	def gen_verification_token(self, user):
		"""Create JWT token that the user can user to veryfy its account."""
		exp_date= timezone.now() + timedelta(days=3)
		payload = {
			'user': user.username,
			'exp': int(exp_date.timestamp()),
			'type': 'email_confirmation',		
		}
		token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
		return token


class UserLoginSerializer(serializers.Serializer):
	"""User Login Serializer.
	Handle the login request data.
	"""
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		"""Verify credentials"""
		user = authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Invalid Credentials')
		if not user.is_verified:
			raise serializers.ValidationError('Account is not active yet. Please verify your email')
		self.context['user'] = user
		return data

	def create(self, data):
		"""Geneate or retrieve a new token."""
		token, created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
	"""Acount Verification Serializer"""
	token = serializers.CharField()

	def validate_token(self, data):
		"""Verify that tokin is valid"""
		try:
			payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError as exp_error:
			raise serializers.ValidationError('Token has expired. ', exp_error)
		except jwt.PyJWTError as error:
			raise serializers.ValidationError('Invalid Token')
		if payload['type'] != 'email_confirmation':
			raise serializers.ValidationError('Token type invalid')

		self.context['payload'] = payload
		return data

	def save(self):
		""" Update user's is_verified status"""
		payload = self.context['payload']
		user = User.objects.get(username=payload['user'])
		user.is_verified=True
		user.save()






