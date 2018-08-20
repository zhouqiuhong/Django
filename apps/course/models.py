# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from organization.models import CourseOrganization, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrganization, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(choices=(('chuji', u'初级'), ('zhongji', u'中级'), ('gaoji', u'高级')), max_length=10)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="image/%Y/%m", verbose_name=u"封面图片", max_length=200)
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=20, verbose_name=u"课程类别", default="")
    tag = models.CharField(default="", max_length=10, verbose_name=u"课程标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    you_need_know = models.CharField(max_length=300, default="", verbose_name=u"课程须知")
    teacher_tell = models.CharField(max_length=300, default="", verbose_name=u"老师告诉你")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_kczj_nums(self):
        """课程章节数目"""
        return self.lesson_set.all().count()

    def get_learn_user(self):
        """获取学习用户"""
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        """获取课程的所有章节"""
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    # url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"视频名称")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    name = models.CharField(max_length=100, verbose_name=u"资源名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=200)
    add_time = models.DateTimeField(max_length=200, default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



