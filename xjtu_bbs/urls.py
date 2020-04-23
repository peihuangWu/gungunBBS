"""xjtu_bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from bbs.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', IndexView.as_view()),
    url(r"^index/$", IndexView.as_view(), name="index"),
    url(r'^classification/(?P<type>\w+)/$', ClassificationView.as_view(), name="classification"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r"^publish/$", PublishView.as_view(), name="publish"),
    url(r"^post/(?P<id>\d+)/$", PostView.as_view(), name="post"),
    url(r"^reply/(?P<post_id>\d+)/$", ReplyView.as_view(), name="reply"),
    url(r"^search/$", SearchView.as_view(), name="search"),
    url(r"^delete/(?P<id>\d+)/$", DeleteView.as_view(), name="delete"),
]
