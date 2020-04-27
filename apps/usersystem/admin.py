from django.contrib import admin

from .models import *


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'follower']
    search_fields = ['user', 'follower']
    list_filter = ['user', 'follower']


# class UserPrivacyAdmin(admin.ModelAdmin):
#     list_display = ['user', "reply", "publish", "follow", "fans"]
#     search_fields = ['user', "reply", "publish", "follow", "fans"]
#     list_filter = ['user', "reply", "publish", "follow", "fans"]


admin.site.register(UserFollow, UserFollowAdmin)
# admin.site.register(UserPrivacy, UserPrivacyAdmin)
