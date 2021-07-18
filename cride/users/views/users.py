"""Users Views"""

#Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Serializers
from cride.users.serializers import (
	UserLoginSerializer,
	UserModelSerializer,
	UserSignUpSerializer,
	AccountVerificationSerializer
)


class UserLoginAPIView(APIView):
	"""User Login Api View"""
	def post(self, request, *args, **kwargs):
		"""Handle Http POST request"""
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		data = {
			'user': UserModelSerializer(user).data,
			'access_token': token
			}
		return Response(data, status=status.HTTP_201_CREATED)


class UserSignUpAPIView(APIView):
	"""Signup Api View"""
	def post(self, request, *args, **kwargs):
		"""Handle Http POST request"""
		serializer = UserSignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)

class AccountVerificationAPIView(APIView):
	"""Acount verification APIVIEW"""
	def post(self, request, *args, **kwargs):
		"""Handle Http POST request"""
		serializer = AccountVerificationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = {'messaje': 'Verification succedded'}
		return Response(data, status=status.HTTP_200_OK)
