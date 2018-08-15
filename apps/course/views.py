from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from .models import Course
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator


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
        tag = course.tag
        if tag:
           #存在隐患：可能会返回它本身
            related_course = Course.objects.filter(tag=tag)[:1]
        else:
            related_course = []

        return render(request, "course-detail.html", {
            "course": course,
            "related_course": related_course,
        })

