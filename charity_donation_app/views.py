from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from charity_donation_app.models import Donation, Institution, Category
from django.db.models import Sum


class LandingPageView(View):
    """Create a main form and display it on the GET method page"""

    def get(self, request):
        total = Donation.objects.aggregate(Sum('quantity'))
        counter_institution = Donation.objects.values('institution').distinct().count()
        fundation = Institution.objects.filter(type=1).order_by('name')
        organization = Institution.objects.filter(type=2).order_by('name')
        local = Institution.objects.filter(type=3).order_by('name')

        paginator1 = Paginator(fundation, 3)
        page_1 = request.GET.get('page')

        fundations = paginator1.get_page(page_1)
        paginator2 = Paginator(organization, 3)
        page_2 = request.GET.get('page')
        organizations = paginator2.get_page(page_2)
        paginator3 = Paginator(local, 3)
        page_3 = request.GET.get('page')
        locs = paginator3.get_page(page_3)
        categories = Category.objects.all()
        return render(request, "index.html", context={"total": total,
                                                      "counter_institution": counter_institution,
                                                      "fundation": fundation,
                                                      "organization": organization,
                                                      "local": local,
                                                      "fundations": fundations,
                                                      "organizations": organizations,
                                                      "locs": locs,
                                                      "categories": categories})


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        name = request.POST.get('name')
