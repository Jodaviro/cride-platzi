"""Circle model admin"""

#django
from django.contrib import admin

#model
from cride.circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
	"""Circle Admin"""
	list_display = ('name', 'slug_name', 'is_public', 'is_limited', 'members_limit', 'is_verified',)
	search_fields = ('slug_name', 'name')
	list_filter = ('is_public', 'is_verified', 'is_limited')