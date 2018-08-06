from django.shortcuts import render

from .models import CourseOrganization, City

from django.views import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class OrgView(View):
    """课程机构列表功能"""

    def get(self, request):
        # 课程机构
        all_org = CourseOrganization.objects.all()
        #机构数量
        org_nums = all_org.count()
        # 城市
        all_city = City.objects.all()
        city_id = request.GET.get("city_id", "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
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
        })