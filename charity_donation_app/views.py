from django.shortcuts import render
from django.views import View

from charity_donation_app.models import Donation, Institution
from django.db.models import Sum


class LandingPageView(View):
    """Create a main form and display it on the GET method page"""

    def get(self, request):
        total = Donation.objects.aggregate(Sum('quantity'))
        counter_institution = Donation.objects.values('institution').distinct().count()
        fundation = Institution.objects.filter(type=1).order_by('name')
        organization = Institution.objects.filter(type=2).order_by('name')
        local = Institution.objects.filter(type=3).order_by('name')
        return render(request, "index.html", context={"total": total,
                                                      "counter_institution": counter_institution,
                                                      "fundation": fundation,
                                                      "organization": organization,
                                                      "local": local,
                                                      })


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")
