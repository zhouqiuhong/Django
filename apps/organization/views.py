from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import CourseOrganization, City, Teacher

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
        #机构搜索
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_org = all_org.filter(Q(name__icontains=search_keywords) | Q(desc_organization__icontains=search_keywords))
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
        # for org in orgs:
        #     print(org.image)

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
        course_org.click_num += 1
        course_org.save()
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
            """如果用户取消收藏，将收藏人数减一"""
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_num -= 1
                #避免出现负数
                if course.fav_num < 0:
                    course.fav_num = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrganization.objects.get(id=int(fav_id))
                org.fav_num -= 1
                # 避免出现负数
                if org.fav_num < 0:
                    org.fav_num = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                # 避免出现负数
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    """课程老师列表"""
    def get(self, request):
        all_teachers = Teacher.objects.all()
        #讲师搜索
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_num")
        sorted_teacher = Teacher.objects.all().order_by("-click_num")
        #对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, per_page=1, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "sorted_teacher": sorted_teacher,
            "sort": sort,
        })


class TeacherDetailView(View):
    """讲师详情页面"""
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        current_nav = "teacher"
        all_course = Course.objects.filter(teacher=teacher)
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]
        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_fav = True
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_course": all_course,
            "sorted_teacher": sorted_teacher,
            "has_teacher_fav": has_teacher_fav,
            "has_org_fav": has_org_fav,
            "current_nav": current_nav,
        })