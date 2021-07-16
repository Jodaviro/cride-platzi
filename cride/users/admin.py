"""Users model admin"""

#django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#users models
from cride.users.models import User, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	"""Profile Model Admin"""
	list_display = ('user', 'reputation', 'rides_taken', 'rides_offered', 'biography',)
	search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
	list_filter = ('reputation',)


class ProfileInLine(admin.StackedInline):
	"""Inline Profile Model"""
	model = Profile
	can_delete = False
	verbose_name_plural = 'profiles'

class CustomUserAdmin(UserAdmin):
	""" Custom User admin """
	inlines = (ProfileInLine,)
	list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client', 'is_verified')
	list_filter = ('is_client', 'is_staff', 'created', 'modified',)

admin.site.register(User, CustomUserAdmin)



