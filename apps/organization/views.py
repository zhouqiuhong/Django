from django.shortcuts import render
from django.http import HttpResponse

from .models import CourseOrganization, City

from django.views import View
from operation.models import UserFavorite
from .forms import UserAskForm
from course.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class OrgView(View):
    """课程机构列表功能"""

    def get(self, request):
        # 课程机构
        all_org = CourseOrganization.objects.all()
        hot_org = all_org.order_by('-click_num')[:3]
        #机构数量
        org_nums = all_org.count()
        # 城市
        all_city = City.objects.all()
        #取出筛选城市
        city_id = request.GET.get("city", "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        #取出筛选类别
        category = request.GET.get("ct", "")
        if category:
            all_org = all_org.filter(category=category)

        #
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_org = all_org.order_by("-students")
            elif sort == "courses":
                all_org = all_org.order_by("-course_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_org, per_page=5, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_org": orgs,
            "all_city": all_city,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_org": hot_org,
            'sort': sort,
        })


class UserAskView(View):
    """用户咨询"""
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错了"}', content_type="application/json")
            # return HttpResponse("{'status':'fail', 'msg':{0}}".format(userask_form.errors))


class OrgHomeView(View):
    """机构首页"""
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    """机构课程首页"""
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """机构介绍首页"""
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """机构介绍首页"""

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            "course_org": course_org,
            "current_page": current_page,
            "all_teachers": all_teachers,
            "has_fav": has_fav,
        })


class AddFavView(View):
    """用户收藏，用户取消收藏"""
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)
        if not request.user.is_authenticated():
            """判断用户登录状态"""
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            """如果记录已经存在，则表示用户取消收藏"""
            exist_record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                # user = user_fav.user
                # print(user)
                # print(int(fav_id))
                # print(int(fav_type))
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")







