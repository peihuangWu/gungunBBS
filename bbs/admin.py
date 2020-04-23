from django.contrib import admin

from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']
    list_filter = ['username']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', "type", "author", "publish_time", "click_num", "reply_num"]
    search_fields = ['title', "type", "publish_time", "click_num", "reply_num", "content"]
    list_filter = ["click_num", "reply_num"]


class ReplyAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "publish_time"]
    search_fields = ["publish_time", "click_num"]


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
