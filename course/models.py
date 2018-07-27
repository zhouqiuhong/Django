# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100,verbose_name=u"课程名")
    desc = models.CharField(max_length=300,verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(('chuji', u'初级'), ('zhongji', u'中级'), ('gaoji', u'高级')), max_length=2)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_num = models.IntegerField(default=0,verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="image/%Y/%m",verbose_name=u"封面图片", max_length=200)
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Vedio(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"视频名称")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"视频名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    name = models.CharField(max_length=100, verbose_name=u"资源名称")
    download = models.ImageField(upload_to="image/%Y/%m", verbose_name=u"资源文件", max_length=200)
    add_time = models.DateTimeField(max_length=200, default=datetime.now)

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name



