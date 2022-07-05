from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from django.urls import reverse

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
    """View created for log in user. This view authenticating and, after that login user."""

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            existing_email = User.objects.filter(email=username)
            if user is not None:
                login(request, user)
                url = request.GET.get('next', '/')
                return redirect(url)
            elif not existing_email:
                return redirect(reverse('register'))
            else:
                new_form = LoginForm()
                return render(request, "login.html", context={"form": new_form,
                                                              "message": "Podano błędne dane!"})


class LogoutView(View):
    """ View created to log out user. """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            users = User.objects.all()
            existing = False
            for us in users:
                if us.username == email:
                    existing = True
            if existing:
                return HttpResponse("User with that username is just existing")
            else:
                if password1 == password2:
                    user = User.objects.create_user(username=email, email=email,
                                            first_name=first_name, last_name=last_name,
                                            password=password1)
                return redirect('login')
        return render(request, "login.html", {"form": form})
