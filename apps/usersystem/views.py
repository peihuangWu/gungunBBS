import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from .models import *


# Create your views here.
class PersonalInfoView(View):
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
            posts = Post.objects.filter(id__in=post_ids).order_by("-publish_time")
        elif type == 2:
            posts = Post.objects.filter(author=request.user).order_by("-publish_time")
        else:
            collects = UserCollect.objects.filter(user=request.user).order_by("-collect_time")
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

        if type == 1 or type == 2:
            for post in posts:
                post.type_name = class_map[post.type]
            post_count = posts.count()
        else:
            for collect in collects:
                collect.post.type_name = class_map[collect.post.type]
            post_count = collects.count()

        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except PageNotAnInteger:
            page = 1
        if page < 0:
            page = 1

        if type == 1 or type == 2:
            p = Paginator(posts, 10, request=request)
            posts = p.page(page).object_list
        else:
            p = Paginator(collects, 10, request=request)
            collects = p.page(page).object_list

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
        elif type == 2:
            return render(request, 'personal_dynamic.html', {
                "publish_posts": posts,
                "type": type,
                "page": page,
                "page_num": page_num,
                "user": request.user,
            })
        else:
            return render(request, 'personal_dynamic.html', {
                "collect_posts": collects,
                "type": type,
                "page": page,
                "page_num": page_num,
                "user": request.user,
            })


class PersonalFollowView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        try:
            nav_tab = int(request.GET.get("tab", 1))
        except Exception:
            nav_tab = 1

        if nav_tab == 1:
            user_follows = UserFollow.objects.filter(user=request.user)
            person_count = user_follows.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(user_follows, 10, request=request)
            user_follows = p.page(page).object_list
            page_num = int(person_count / 10)
            if person_count % 10 != 0:
                page_num += 1

            return render(request, "personal_follow.html", {
                "user_follows": user_follows,
                "nav_tab": nav_tab,
                "page": page,
                "page_num": page_num,
                "num": person_count,
                "user": request.user,
            })
        else:
            topic_follows = TopicFollow.objects.filter(user=request.user)
            topic_count = topic_follows.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(topic_follows, 10, request=request)
            topic_follows = p.page(page).object_list
            page_num = int(topic_count / 10)
            if topic_count % 10 != 0:
                page_num += 1

            return render(request, "personal_follow.html", {
                "topic_follows": topic_follows,
                "nav_tab": nav_tab,
                "page": page,
                "page_num": page_num,
                "num": topic_count,
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
            "user": request.user,
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

        colleges = ["电气工程学院", "机械工程学院", "理学院", "能源与动力工程学院", "电子与信息工程学院",
                        "法学院", "航天航空学院", "材料科学与工程学院", "软件学院", "人居环境与建筑工程学院",
                        "生命科学与技术学院", "医学部", "经济与金融学院", "公共政策与管理学院", "管理学院",
                        "人文社会科学学院", "软件学院", "金禾经济研究中心", "外国语学院", "前沿科学技术研究院",
                        "数学与统计学院", "化学工程与技术学院", "体育中心", "马克思主义学院", "可持续发展学院",
                        "国际教育学院", "继续教育学院", "网络教育学院"]

        person.collegeName = colleges[person.college]
        isFans = UserFollow.objects.filter(user=request.user, follower=person).count() > 0

        if type == 1:
            person.privacy = person.reply_authority
            replys = Reply.objects.filter(author=person)
            post_ids = []
            for reply in replys:
                post_ids.append(reply.post.id)
            replyed_posts = Post.objects.filter(id__in=post_ids).order_by("-publish_time")

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
                "type": type,
            })

        elif type == 2:
            person.privacy = person.publish_authority
            publish_posts = Post.objects.filter(author=person).order_by("-publish_time")

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
                "type": type,
            })
        elif type == 3:
            person.privacy = person.follow_authority
            user_follows = UserFollow.objects.filter(user=person).order_by("-follow_time")
            followers_count = user_follows.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(user_follows, 10, request=request)
            user_follows = p.page(page).object_list
            page_num = int(followers_count / 10)
            if followers_count % 10 != 0:
                page_num += 1

            return render(request, "personal_page_by_other.html", {
                "user": request.user,
                "person": person,
                "isFans": isFans,
                "user_follows": user_follows,
                "page": page,
                "page_num": page_num,
                "num": followers_count,
                "type": type,
            })

        else:
            person.privacy = person.fans_authority
            user_by_follows = UserFollow.objects.filter(follower=person).order_by("-follow_time")
            fans_count = user_by_follows.count()
            try:
                page = request.GET.get('page', 1)
                page = int(page)
            except PageNotAnInteger:
                page = 1
            if page < 0:
                page = 1

            p = Paginator(user_by_follows, 10, request=request)
            user_by_follows = p.page(page).object_list
            page_num = int(fans_count / 10)
            if fans_count % 10 != 0:
                page_num += 1

            return render(request, "personal_page_by_other.html", {
                "user": request.user,
                "person": person,
                "isFans": isFans,
                "user_by_follows": user_by_follows,
                "page": page,
                "page_num": page_num,
                "num": fans_count,
                "type": type,
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
            return render(request, "personal_password.html", {"msg": "请输入原密码！"})

        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return render(request, "personal_password.html", {"msg": "两次新密码不匹配！"})
            if len(password1) < 5:
                return render(request, "personal_password.html", {"msg": "密码不能小于5位！"})
            user.password = make_password(password1)
            user.save()
            return HttpResponseRedirect(reverse("personal_password"))
        else:
            return render(request, "personal_password.html", {"msg": "原密码输入错误！"})


class FollowView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))

        data = json.loads(request.body)
        type = data["type"]
        follower_id = data["followerId"]
        try:
            follower = User.objects.get(id=follower_id)
        except Exception:
            return JsonResponse({'status': 2, 'msg': 'error'})

        if type == 1:
            if UserFollow.objects.filter(user=request.user, follower=follower):
                return JsonResponse({'status': 2, 'msg': 'error'})
            user_follow = UserFollow()
            user_follow.user = request.user
            user_follow.follower = follower
            user_follow.save()
            follower.un_read_fans_num += 1
            follower.save()
            return JsonResponse({'status': 1, 'msg': 'success'})
        else:
            try:
                user_follow = UserFollow.objects.get(user=request.user, follower=follower)
            except Exception:
                return JsonResponse({'status': 2, 'msg': 'error'})
            user_follow.delete()
            return JsonResponse({'status': 1, 'msg': 'success'})


class PersonalMessageView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        try:
            type = int(request.GET.get("type", 1))
        except Exception:
            type = 1

        if type == 1:
            user_posts = Post.objects.filter(author=request.user)
            replys = Reply.objects.filter(post__in=user_posts).exclude(author=request.user).order_by("-publish_time")
            request.user.un_read_reply_num = 0
            request.user.save()
            return render(request, "personal_message.html", {
                "user": request.user,
                "type": type,
                "replys": replys,
            })
        else:
            user_follows = UserFollow.objects.filter(follower=request.user).order_by("-follow_time")
            request.user.un_read_fans_num = 0
            request.user.save()
            return render(request, "personal_message.html", {
                "user": request.user,
                "type": type,
                "user_follows": user_follows,
            })


class CollectView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse("login"))
        try:
            id = int(request.GET.get("id", 0))
        except Exception:
            id = 0

        try:
            post_info = Post.objects.get(id=id)
        except Exception:
            return JsonResponse({'status': 2, 'msg': 'error'})

        user_collect = UserCollect.objects.filter(user=request.user, post=post_info)
        if user_collect:
            user_collect.delete()
            return JsonResponse({'status': 1, 'msg': 'success'})

        user_collect = UserCollect()
        user_collect.user = request.user
        user_collect.post = post_info
        user_collect.save()
        return JsonResponse({'status': 1, 'msg': 'success'})