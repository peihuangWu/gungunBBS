import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import *


# Create your views here.
class PersonalInfoView(View):
    # def __new__(cls, *args, **kwargs):
    #     cls.colleges = ["电气工程学院", "机械工程学院", "理学院", "能源与动力工程学院", "电子与信息工程学院",
    #                     "法学院", "航天航空学院", "材料科学与工程学院", "软件学院", "人居环境与建筑工程学院",
    #                     "生命科学与技术学院", "医学部", "经济与金融学院", "公共政策与管理学院", "管理学院",
    #                     "人文社会科学学院", "软件学院", "金禾经济研究中心", "外国语学院", "前沿科学技术研究院",
    #                     "数学与统计学院", "化学工程与技术学院", "体育中心", "马克思主义学院", "可持续发展学院",
    #                     "国际教育学院", "继续教育学院", "网络教育学院"]

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        return render(request, "personal_info.html", {
            "user": request.user
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        gender = request.POST.get("gender", "male")
        if gender == "male":
            gender = "男"
        else:
            gender = "女"
        try:
            college = int(request.POST.get("college", 0))
            if college < 0 or college > 27:
                college = 0
        except:
            college = 0
        try:
            year = int(request.POST.get("year", 1990))
        except Exception:
            year = 1990
        try:
            month = int(request.POST.get("month", 1))
        except Exception:
            month = 1
        emotion = request.POST.get("emotion", "single")
        if emotion == "single":
            emotion = "单身"
        elif emotion == "in_object":
            emotion = "交往中"
        elif emotion == "married":
            emotion = "已婚"
        else:
            emotion = "丧偶"
        sign = request.POST.get("sign", "")

        request.user.gender = gender
        request.user.college = college
        request.user.birth_year = year
        request.user.birth_month = month
        request.user.emotion = emotion
        request.user.sign = sign
        request.user.save()
        return HttpResponseRedirect(reverse("personal_info"))


class PersonalPortraitView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        return render(request, "personal_portrait.html", {
            "user": request.user
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        data = json.loads(request.body)
        request.user.portrait = data["img"]
        request.user.save()
        return JsonResponse({'status': 1, 'msg': 'success'})


class PersonalDynamicView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        try:
            type = int(request.GET.get("type", 1))
        except:
            type = 1

        if type == 1:
            replys = Reply.objects.filter(author=request.user)
            post_ids = []
            for reply in replys:
                post_ids.append(reply.post.id)
            posts = Post.objects.filter(id__in=post_ids)
        else:
            posts = Post.objects.filter(author=request.user)

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
            post.type_name = class_map[post.type]

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

        if type == 1:
            return render(request, 'personal_dynamic.html', {
                "reply_posts": posts,
                "type": type,
                "page": page,
                "page_num": page_num,
                "user": request.user,
            })


class PersonalFollowView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        user_follows = UserFollow.objects.filter(user=request.user)
        person_ids = []
        for user_follow in user_follows:
            person_ids.append(user_follow.follower.id)
        persons = User.objects.filter(id__in=person_ids)

        person_count = persons.count()
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1

        p = Paginator(persons, 10, request=request)
        persons = p.page(page).object_list
        page_num = int(person_count / 10)
        if person_count % 10 != 0:
            page_num += 1

        return render(request, "personal_follow.html", {
            "persons": persons,
            "page": page,
            "page_num": page_num,
            "num": person_count,
            "user": request.user,
        })


class PersonalFansView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        user_fans = UserFollow.objects.filter(follower=request.user)
        person_ids = []
        for user_fan in user_fans:
            person_ids.append(user_fan.user.id)
        persons = User.objects.filter(id__in=person_ids)

        person_count = persons.count()
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1

        p = Paginator(persons, 10, request=request)
        persons = p.page(page).object_list
        page_num = int(person_count / 10)
        if person_count % 10 != 0:
            page_num += 1

        return render(request, "personal_fans.html", {
            "persons": persons,
            "page": page,
            "page_num": page_num,
            "num": person_count,
            "user": request.user,
        })


class PersonalPrivacyView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        return render(request, "personal_privacy.html", {
            "user": request.user
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        try:
           reply_authority = int(request.POST.get("reply"))
        except Exception:
            reply_authority = 3

        try:
           publish_authority = int(request.POST.get("publish"))
        except Exception:
            publish_authority = 3

        try:
           follow_authority = int(request.POST.get("follow"))
        except Exception:
            follow_authority = 3

        try:
            fans_authority = int(request.POST.get("fans"))
        except Exception:
            fans_authority = 3

        request.user.reply_authority = reply_authority
        request.user.publish_authority = publish_authority
        request.user.follow_authority = follow_authority
        request.user.fans_authority = fans_authority
        request.user.save()
        return HttpResponseRedirect(reverse("personal_privacy"))


class PersonalPageByOtherView(View):
    def __new__(cls, *args, **kwargs):
        cls.colleges = ["电气工程学院", "机械工程学院", "理学院", "能源与动力工程学院", "电子与信息工程学院",
                        "法学院", "航天航空学院", "材料科学与工程学院", "软件学院", "人居环境与建筑工程学院",
                        "生命科学与技术学院", "医学部", "经济与金融学院", "公共政策与管理学院", "管理学院",
                        "人文社会科学学院", "软件学院", "金禾经济研究中心", "外国语学院", "前沿科学技术研究院",
                        "数学与统计学院", "化学工程与技术学院", "体育中心", "马克思主义学院", "可持续发展学院",
                        "国际教育学院", "继续教育学院", "网络教育学院"]

    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        try:
            type = int(request.GET.get("type", 1))
        except Exception:
            type = 1

        try:
            person = User.objects.get(id=id)
        except:
            return HttpResponseRedirect("index")

        person.collegeName = self.__class__.colleges[person.college]
        isFans = UserFollow.objects.filter(user=request.user, follower=person).count() > 0

        if type == 1:
            person.privacy = person.reply_authority
            replys = Reply.objects.filter(author=person)
            post_ids = []
            for reply in replys:
                post_ids.append(reply.post.id)
            replyed_posts = Post.objects.filter(id__in=post_ids)

            replyed_posts_count = replyed_posts.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(replyed_posts, 10, request=request)
            replyed_posts = p.page(page).object_list
            page_num = int(replyed_posts_count / 10)
            if replyed_posts_count % 10 != 0:
                page_num += 1

            return render(request, "personal_page_by_other.html", {
                "user": request.user,
                "person": person,
                "isFans": isFans,
                "replyed_posts": replyed_posts,
                "page": page,
                "page_num": page_num,
            })

        elif type == 2:
            person.privacy = person.publish_authority
            publish_posts = Post.objects.filter(author=person)

            publish_posts_count = publish_posts.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(publish_posts, 10, request=request)
            publish_posts = p.page(page).object_list
            page_num = int(publish_posts_count / 10)
            if publish_posts_count % 10 != 0:
                page_num += 1

            return render(request, "personal_page_by_other.html", {
                "user": request.user,
                "person": person,
                "isFans": isFans,
                "publish_posts": publish_posts,
                "page": page,
                "page_num": page_num,
            })
        elif type == 3:
            person.privacy = person.follow_authority
            user_follows = UserFollow.objects.filter(user=person)
            person_ids = []
            for user_follow in user_follows:
                person_ids.append(user_follow.follower.id)
            followers = User.objects.filter(id__in=person_ids)

            followers_count = followers.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(followers, 10, request=request)
            followers = p.page(page).object_list
            page_num = int(followers_count / 10)
            if followers_count % 10 != 0:
                page_num += 1

            return render(request, "personal_page_by_other.html", {
                "user": request.user,
                "person": person,
                "isFans": isFans,
                "followers": followers,
                "page": page,
                "page_num": page_num,
                "num": followers_count,
            })

        else:
            person.privacy = person.fans_authority
            user_fans = UserFollow.objects.filter(follower=person)
            person_ids = []
            for user_fan in user_fans:
                person_ids.append(user_fan.user.id)
            fans_list = User.objects.filter(id__in=person_ids)

            fans_count = fans_list.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(fans_list, 10, request=request)
            fans_list = p.page(page).object_list
            page_num = int(fans_count / 10)
            if fans_count % 10 != 0:
                page_num += 1

            return render(request, "personal_page_by_other.html", {
                "user": request.user,
                "person": person,
                "isFans": isFans,
                "fans_list": fans_list,
                "page": page,
                "page_num": page_num,
                "num": fans_count,
            })


class PersonalPasswordView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        return render(request, "personal_password.html", {
            "user": request.user
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        password = request.POST.get("password", "")
        if password == "":
            return HttpResponseRedirect(reverse("personal_password"))

        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return HttpResponseRedirect(reverse("personal_password"))
            if len(password1) < 5:
                return HttpResponseRedirect(reverse("personal_password"))
            user.password = make_password(password1)
            user.save()
            return HttpResponseRedirect(reverse("personal_password"))
        else:
            return HttpResponseRedirect(reverse("personal_password"))
