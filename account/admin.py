from django.contrib import admin
from account.models import UserProfile, UserMeta

admin.site.register(UserProfile)
admin.site.register(UserMeta)
