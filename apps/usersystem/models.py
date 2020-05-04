from datetime import datetime

from django.db import models

from bbs.models import *

# Create your models here.


class UserFollow(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, verbose_name="用户", null=True, blank=True)
    follower = models.ForeignKey(User, related_name="be_follow_user", on_delete=models.CASCADE, verbose_name="被关注者", null=True, blank=True)
    follow_time = models.DateTimeField(default=datetime.now, verbose_name="关注时间")
    hasRead = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "用户关注表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user + "->" + self.follower


class UserCollect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="帖子", null=True, blank=True)
    collect_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "用户收藏表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user + "->" + self.post


# class UserPrivacy(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", null=True, blank=True)
#     reply = models.IntegerField(default=3, verbose_name="我的回复访问权限")
#     publish = models.IntegerField(default=3, verbose_name="我的发表访问权限")
#     follow = models.IntegerField(default=3, verbose_name="我的关注访问权限")
#     fans = models.IntegerField(default=3, verbose_name="我的粉丝访问权限")
#
#     class Meta:
#         verbose_name = "用户隐私设置表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.user
