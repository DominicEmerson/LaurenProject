# Register your models here.
from django.contrib import admin
from .models import User, Community, CommunityMembership, Event, EventAttendance, Post, Permission
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(User)
admin.site.register(Community)
admin.site.register(CommunityMembership)
admin.site.register(Event)
admin.site.register(EventAttendance)
admin.site.register(Post)
admin.site.register(Permission)