from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from .models import Course, CourseResource, Video
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models.query import Q


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]
        #课程搜索
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                           Q(detail__icontains=search_keywords))#icontains中i不区分大小写

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


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)


        user_ids = [user_course.user.id for user_course in user_courses]
        #获取学过该课程的所有用户
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        #获取相关的课程信息
        related_course = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        all_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "all_resource": all_resource,
            "related_course": related_course,

        })


class CourseCommentView(LoginRequiredMixin, View):
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


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)

        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取学过该课程的所有用户
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        # 获取相关的课程信息
        related_course = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        all_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "all_resource": all_resource,
            "related_course": related_course,
            "video": video,

        })


# class TeacherListView(View):
#     def get(self, request, teacher_id):
#         pass