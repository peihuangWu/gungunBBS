import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import *
from usersystem.models import *
from .forms import *


# Create your views here.
class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        banners = Banner.objects.all().order_by("-add_time")[:3]
        posts = Post.objects.all().order_by("-publish_time")[:10]
        class_map = {
            "生活专区": "live",
            "学习专区": "study",
            "就业专区": "job",
            "闲聊专区": "chat",
            "时事专区": "news",
            "运动专区": "sport",
            "游戏专区": "game",
            "电影专区": "movie",
            "音乐专区": "music",
            "旅游专区": "tour"
        }
        for post in posts:
            post.type2 = class_map.get(post.type, "live")

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        return render(request, 'index.html', {
            "user": request.user,
            "banners": banners,
            "posts": posts,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
        })


class ClassificationView(View):
    def get(self, request, type):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        oldtype = type
        if type == "study":
            type = "学习专区"
        elif type == "job":
            type = "就业专区"
        elif type == "chat":
            type = "闲聊专区"
        elif type == "news":
            type = "时事专区"
        elif type == "sport":
            type = "运动专区"
        elif type == "game":
            type = "游戏专区"
        elif type == "movie":
            type = "电影专区"
        elif type == "music":
            type = "音乐专区"
        elif type == "tour":
            type = "旅游专区"
        else:
            type = "生活专区"

        try:
            nav_tab = int(request.GET.get('tab', 1))
        except Exception:
            nav_tab = 1

        if nav_tab == 1:
            posts = Post.objects.filter(type=type).order_by("-publish_time")
        elif nav_tab == 2:
            posts = Post.objects.filter(type=type, is_boutique=True).order_by("-publish_time")
        elif nav_tab == 3:
            posts = Post.objects.filter(type=type, reply_num__gt=10, click_num__gt=100).order_by("-publish_time")

        post_count = posts.count()
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1

        p = Paginator(posts, 10, request=request)
        posts = p.page(page).object_list
        page_num = int(post_count / 10)
        if post_count % 10 != 0:
            page_num += 1

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        return render(request, 'area.html', {
            "posts": posts,
            "type": oldtype,
            "page": page,
            "page_num": page_num,
            "nav_tab": nav_tab,
            "user": request.user,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
        })


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"msg": "请输入合法的用户名或密码"})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html", {})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return render(request, "register.html", {"msg": "两次输入的密码不匹配"})
            username = request.POST.get("username", "")
            if User.objects.filter(username=username):
                return render(request, "register.html", {"msg": "用户已经存在"})
            user = User()
            user.username = username
            user.password = make_password(password1)
            user.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            return render(request, "register.html", {"msg": "请输入合法的用户名或密码"})


class PublishView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        return render(request, "publish_post.html", {
            "user": request.user,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        body = json.loads(request.body)
        title = body.get("title", "")
        type = body.get("classification", "")
        content = json.dumps(body.get("content", ""))
        if title == "":
            title = "我发布了一条帖子，大家快来看看吧~"
        if type == "study":
            type = "学习专区"
        elif type == "job":
            type = "就业专区"
        elif type == "chat":
            type = "闲聊专区"
        elif type == "news":
            type = "时事专区"
        elif type == "sport":
            type = "运动专区"
        elif type == "game":
            type = "游戏专区"
        elif type == "movie":
            type = "电影专区"
        elif type == "music":
            type = "音乐专区"
        elif type == "tour":
            type = "旅游专区"
        else:
            type = "生活专区"
        post_info = Post()
        post_info.title = title
        post_info.type = type
        post_info.author = request.user
        post_info.click_num = 0
        post_info.content = content
        post_info.is_boutique = False
        post_info.reply_num = 0
        post_info.save()
        return HttpResponseRedirect(reverse("classification", kwargs={'type': request.POST.get("classification", "live")}))


class PostView(View):
    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        try:
            post_info = Post.objects.get(id=id)
        except Exception:
            return render(request, "404.html")
        post_info.click_num += 1
        post_info.save()
        replys = Reply.objects.filter(post=post_info)
        replys_count = replys.count()
        try:
            page = request.GET.get("page", 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1
        p = Paginator(replys, 10, request=request)
        replys = p.page(page).object_list
        page_num = int(replys_count / 10)
        if replys_count % 10 != 0:
            page_num += 1

        for i, reply in enumerate(replys, 2):
            reply.num = (page - 1) * 10 + i

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        if UserCollect.objects.filter(user=request.user, post=post_info):
            hasCollect = True
        else:
            hasCollect = False

        return render(request, "post_detail.html", {
            "post_info": post_info,
            "replys": replys,
            "page_num": page_num,
            "page": page,
            "user": request.user,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
            "hasCollect": hasCollect,
        })


class ReplyView(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        post_info = Post.objects.get(id=post_id)
        content = json.dumps(json.loads(request.body)["content"])
        if not post_info:
            return
        if not content:
            return
        post_info.reply_num += 1
        post_info.save()
        reply = Reply()
        reply.post = post_info
        reply.author = request.user
        reply.content = content
        reply.save()
        return HttpResponseRedirect(reverse("post", kwargs={'id': post_info.id}))


class SearchView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        search_text = request.GET.get('searchText', "")
        nav_tab = int(request.GET.get('tab', 1))

        if nav_tab == 1:
            posts = Post.objects.filter(Q(title__icontains=search_text) | Q(content__icontains=search_text)).order_by(
                "-publish_time")
        elif nav_tab == 2:
            posts = Post.objects.filter(Q(title__icontains=search_text) | Q(content__icontains=search_text),
                                        is_boutique=True).order_by("-publish_time")
        elif nav_tab == 3:
            posts = Post.objects.filter(Q(title__icontains=search_text) | Q(content__icontains=search_text),
                                        reply_num__gt=10, click_num__gt=100).order_by("-publish_time")
        elif nav_tab == 4:
            users = User.objects.filter(username__icontains=search_text)
        else:
            topics = Topic.objects.filter(name__icontains=search_text)

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1

        if nav_tab == 1 or nav_tab == 2 or nav_tab == 3:
            post_count = posts.count()
            p = Paginator(posts, 10, request=request)
            posts = p.page(page).object_list
            page_num = int(post_count / 10)
            if post_count % 10 != 0:
                page_num += 1
            return render(request, 'area.html', {
                "posts": posts,
                "type": "",
                "page": page,
                "page_num": page_num,
                "user": request.user,
                "nav_tab": nav_tab,
                "searchText": search_text,
                "unReadReplyNum": unReadReplyNum,
                "unReadFansNum": unReadFansNum,
                "unReadMessageNum": unReadMessageNum,
            })
        elif nav_tab == 4:
            user_count = users.count()
            p = Paginator(users, 10, request=request)
            users = p.page(page).object_list
            page_num = int(user_count / 10)
            if user_count % 10 != 0:
                page_num += 1
            return render(request, 'area.html', {
                "users": users,
                "type": "",
                "page": page,
                "page_num": page_num,
                "user": request.user,
                "nav_tab": nav_tab,
                "searchText": search_text,
                "unReadReplyNum": unReadReplyNum,
                "unReadFansNum": unReadFansNum,
                "unReadMessageNum": unReadMessageNum,
            })
        else:
            topic_count = topics.count()
            p = Paginator(topics, 10, request=request)
            topics = p.page(page).object_list
            page_num = int(topic_count / 10)
            if topic_count % 10 != 0:
                page_num += 1
            return render(request, 'area.html', {
                "topics": topics,
                "type": "",
                "page": page,
                "page_num": page_num,
                "user": request.user,
                "nav_tab": nav_tab,
                "searchText": search_text,
                "unReadReplyNum": unReadReplyNum,
                "unReadFansNum": unReadFansNum,
                "unReadMessageNum": unReadMessageNum,
            })


class DeleteView(View):
    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        try:
            post_info = Post.objects.get(id=id)
        except Exception:
            return
        if post_info.author.username != request.user.username:
            return
        post_info.delete()
        return HttpResponseRedirect(reverse("index"))


class PublishTopicView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        data = json.loads(request.body)

        topic_name = data["name"]
        topic = Topic.objects.filter(name=topic_name)
        if topic:
            return JsonResponse({'status': 2, 'msg': 'error', "topic_id": topic[0].id})
        topic = Topic()
        topic.name = topic_name
        topic.save()
        return JsonResponse({'status': 1, 'msg': 'success', "topic_id": topic.id})


class TopicView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        try:
            id = int(request.GET.get("id", 0))
        except:
            id = 0

        try:
            topic = Topic.objects.get(id=id)
        except Exception:
            return HttpResponseRedirect(reverse("index"))

        try:
            nav_tab = int(request.GET.get('tab', 1))
        except Exception:
            nav_tab = 1

        if TopicFollow.objects.filter(user=request.user, topic=topic):
            hasFollow = True
        else:
            hasFollow = False

        if nav_tab == 1:
            posts = TopicPost.objects.filter(topic=topic).order_by("-publish_time")
        elif nav_tab == 2:
            posts = TopicPost.objects.filter(topic=topic, is_boutique=True).order_by("-publish_time")
        elif nav_tab == 3:
            posts = TopicPost.objects.filter(topic=topic, reply_num__gt=10, click_num__gt=100).order_by("-publish_time")

        post_count = posts.count()
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1

        p = Paginator(posts, 10, request=request)
        posts = p.page(page).object_list
        page_num = int(post_count / 10)
        if post_count % 10 != 0:
            page_num += 1

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        return render(request, 'topic.html', {
            "topic": topic,
            "posts": posts,
            "page": page,
            "page_num": page_num,
            "nav_tab": nav_tab,
            "user": request.user,
            "hasFollow": hasFollow,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
        })


class FollowTopicView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        data = json.loads(request.body)
        type = data["type"]
        follower_id = data["followerId"]
        try:
            topic = Topic.objects.get(id=follower_id)
        except Exception:
            return JsonResponse({'status': 2, 'msg': 'error'})

        if type == 1:
            if TopicFollow.objects.filter(user=request.user, topic=topic):
                return JsonResponse({'status': 2, 'msg': 'error'})
            topic_follow = TopicFollow()
            topic_follow.user = request.user
            topic_follow.topic = topic
            topic_follow.save()
            topic.follow_num += 1
            topic.save()
            return JsonResponse({'status': 1, 'msg': 'success'})
        else:
            try:
                topic_follow = TopicFollow.objects.get(user=request.user, topic=topic)
            except Exception:
                return JsonResponse({'status': 2, 'msg': 'error'})
            topic_follow.delete()
            topic.follow_num -= 1
            topic.save()
            return JsonResponse({'status': 1, 'msg': 'success'})


class PublishTopicPostView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        try:
            topic_id = int(request.GET.get("topic_id", 1))
        except Exception:
            topic_id = 1

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        return render(request, "publish_topic_post.html", {
            "user": request.user,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
            "topic_id": topic_id,
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        body = json.loads(request.body)
        title = body.get("title", "")
        content = json.dumps(body.get("content", ""))
        try:
            topic_id = int(body.get("topic_id", 1))
        except Exception:
            topic_id = 1

        try:
            topic = Topic.objects.get(id=topic_id)
        except Exception:
            return HttpResponseRedirect(reverse("topic"))

        post_info = TopicPost()
        post_info.topic = topic
        post_info.title = title
        post_info.author = request.user
        post_info.click_num = 0
        post_info.content = content
        post_info.is_boutique = False
        post_info.reply_num = 0
        post_info.save()
        return HttpResponseRedirect(reverse("topic") + "?id=" + str(topic_id))


class TopicPostView(View):
    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        try:
            post_info = TopicPost.objects.get(id=id)
        except Exception:
            return render(request, "404.html")
        post_info.click_num += 1
        post_info.save()
        replys = TopicReply.objects.filter(post=post_info)
        replys_count = replys.count()
        try:
            page = request.GET.get("page", 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1
        p = Paginator(replys, 10, request=request)
        replys = p.page(page).object_list
        page_num = int(replys_count / 10)
        if replys_count % 10 != 0:
            page_num += 1

        for i, reply in enumerate(replys, 2):
            reply.num = (page - 1) * 10 + i

        user_posts = Post.objects.filter(author=request.user)
        unReadReplyNum = Reply.objects.filter(post__in=user_posts, hasRead=False).count()
        if unReadReplyNum > 99:
            unReadReplyNum = 99
        unReadFansNum = UserFollow.objects.filter(follower=request.user, hasRead=False).count()
        if unReadFansNum > 99:
            unReadFansNum = 99
        unReadMessageNum = unReadReplyNum + unReadFansNum
        if unReadMessageNum > 99:
            unReadMessageNum = 99

        return render(request, "topic_post_detail.html", {
            "post_info": post_info,
            "replys": replys,
            "page_num": page_num,
            "page": page,
            "user": request.user,
            "unReadReplyNum": unReadReplyNum,
            "unReadFansNum": unReadFansNum,
            "unReadMessageNum": unReadMessageNum,
        })


class TopicReplyView(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        post_info = TopicPost.objects.get(id=post_id)
        content = json.dumps(json.loads(request.body)["content"])
        if not post_info:
            return
        if not content:
            return
        post_info.reply_num += 1
        post_info.save()
        reply = TopicReply()
        reply.post = post_info
        reply.author = request.user
        reply.content = content
        reply.save()
        return HttpResponseRedirect(reverse("topic_post", kwargs={'id': post_info.id}))


def page_not_found(request, exception):
    return render(request, '404.html')




