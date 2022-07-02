from django.shortcuts import render
from django.views import View

from charity_donation_app.models import Donation
from django.db.models import Sum


class LandingPageView(View):
    """Create a main form and display it on the GET method page"""

    def get(self, request):
        total = Donation.objects.aggregate(Sum('quantity'))
        counter_institution = Donation.objects.values('institution').distinct().count()
        return render(request, "index.html", context={"total": total,
                                                      "counter_institution": counter_institution})


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")
