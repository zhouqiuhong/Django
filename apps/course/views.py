from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from .models import Course, CourseResource
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_course = all_course.order_by("-students")
            elif sort == "hot":
                all_course = all_course.order_by("-click_num")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, per_page=3, request=request)

        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_course": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        # all_course = Course.objects.all()
        course = Course.objects.get(id=int(course_id))
        """增加课程点击数"""
        course.click_num += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
           #存在隐患：可能会返回它本身
            related_course = Course.objects.filter(tag=tag)[:1]
        else:
            related_course = []

        return render(request, "course-detail.html", {
            "course": course,
            "related_course": related_course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_course = UserCourse.objects.filter(course=course)
        all_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "all_resource": all_resource,
            "user_course": user_course,
        })


class CourseCommntView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # comments = CourseComments.objects.all()
        comments = CourseComments.objects.filter(course=course)
        all_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "comments": comments,
            "all_resource": all_resource,

        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            """判断用户登录状态"""
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        course_id = request.POST.get("course_id", 0)
        comment = request.POST.get("comments", "")
        if int(course_id) > 0 and comment:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comment = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success", "msg":"添加失败"}', content_type='application/json')