from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="昵称", default="")
    type = models.CharField(max_length=20, verbose_name="分区", default="live")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者", null=True, blank=True)
    publish_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    click_num = models.IntegerField(default=0, verbose_name="浏览数")
    reply_num = models.IntegerField(default=0, verbose_name="回复数")
    is_boutique = models.BooleanField(default=False, verbose_name="是否为精品")
    content = models.TextField(default="", verbose_name="内容")

    class Meta:
        verbose_name = "帖子信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="帖子", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者", null=True, blank=True)
    publish_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")
    content = models.TextField(default="", verbose_name="内容")

    class Meta:
        verbose_name = "回复信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

