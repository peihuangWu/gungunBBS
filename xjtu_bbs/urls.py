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
from usersystem.views import *

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
    url(r"^personal_info/$", PersonalInfoView.as_view(), name="personal_info"),
    url(r"^personal_portrait/$", PersonalPortraitView.as_view(), name="personal_portrait"),
    url(r"^personal_dynamic/$", PersonalDynamicView.as_view(), name="personal_dynamic"),
    url(r"^personal_follow/$", PersonalFollowView.as_view(), name="personal_follow"),
    url(r"^personal_fans/$", PersonalFansView.as_view(), name="personal_fans"),
    url(r"^personal_privacy/$", PersonalPrivacyView.as_view(), name="personal_privacy"),
    url(r"^personal_password/$", PersonalPasswordView.as_view(), name="personal_password"),
    url(r"^personal_face/$", PersonalFaceView.as_view(), name="personal_face"),
    url(r"^personal_page_by_other/(?P<id>\d+)/$", PersonalPageByOtherView.as_view(), name="personal_page_by_other"),
    url(r"^follow/$", FollowView.as_view(), name="follow"),
    url(r"^personal_message/$", PersonalMessageView.as_view(), name="personal_message"),
    url(r"^collect/$", CollectView.as_view(), name="collect"),
    url(r"^publish_topic/$", PublishTopicView.as_view(), name="publish_topic"),
    url(r"^topic/$", TopicView.as_view(), name="topic"),
    url(r"^follow_topic/$", FollowTopicView.as_view(), name="follow_topic"),
    url(r"^publish_topic_post/$", PublishTopicPostView.as_view(), name="publish_topic_post"),
    url(r"^topic_post/(?P<id>\d+)/$", TopicPostView.as_view(), name="topic_post"),
    url(r"^topic_reply/(?P<post_id>\d+)/$", TopicReplyView.as_view(), name="topic_reply"),
    url(r"^contribute_face/$", ContributeFaceView.as_view(), name="contribute_face"),
    url(r"^face_list/$", FaceListView.as_view(), name="face_list"),
    url(r"^add_face/$", AddFaceView.as_view(), name="add_face"),
]

# handler404 = 'bbs.views.page_not_found'

