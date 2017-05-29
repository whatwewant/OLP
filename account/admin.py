from django.contrib import admin
from account.models import UserProfile, UserMeta
from account.models import UserInfo, UserLoginHistory

admin.site.register(UserProfile)
admin.site.register(UserMeta)

admin.site.register(UserInfo)
admin.site.register(UserLoginHistory)
