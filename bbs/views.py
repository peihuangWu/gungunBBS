from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import *
from .forms import *


# Create your views here.
class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
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
        return render(request, 'index.html', {
            "posts": posts,
            "username": request.user.username
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

        nav_tab = int(request.GET.get('tab', 1))

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

        return render(request, 'area.html', {
            "posts": posts,
            "type": oldtype,
            "page": page,
            "page_num": page_num,
            "nav_tab": nav_tab,
            "username": request.user.username
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
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            password1 = request.POST.get("password", "")
            password2 = request.POST.get("password", "")
            if password1 != password2:
                return render(request, "register.html", {"register_form": register_form, "msg": "两次输入的密码不匹配"})
            username = request.POST.get("username", "")
            if User.objects.filter(username=username):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            user = User()
            user.username = username
            user.password = make_password(password1)
            user.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class PublishView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        return render(request, "publish_post.html", {
            "username": request.user.username,
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        title = request.POST.get("title", "")
        if title == "":
            title = "我发布了一条帖子，大家快来看看吧~"
        type = request.POST.get("classification", "live")
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
        content = request.POST.get("content", "")
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

        return render(request, "post_detail.html", {
            "post_info": post_info,
            "replys": replys,
            "page_num": page_num,
            "page": page,
            "username": request.user.username
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))


class ReplyView(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        post_info = Post.objects.get(id=post_id)
        content = request.POST.get("content", "")
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

        return render(request, 'area.html', {
            "posts": posts,
            "type": "",
            "page": page,
            "page_num": page_num,
            "username": request.user.username,
            "searchText": search_text,
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

