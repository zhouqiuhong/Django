from django.shortcuts import render
from django.http import HttpResponse

from .models import CourseOrganization, City

from django.views import View

from .forms import UserAskForm

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
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'出错了'}", content_type="application/")
            # return HttpResponse("{'status':'fail', 'msg':{0}}".format(userask_form.errors))