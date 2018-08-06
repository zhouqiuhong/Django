from django.shortcuts import render

from .models import CourseOrganization, City

from django.views import View

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

        return render(request, "org-list.html", {
            "all_org": all_org,
            "all_city": all_city,
            "org_nums": org_nums,
        })