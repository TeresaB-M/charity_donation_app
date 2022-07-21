from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, DonationModelForm
from django.urls import reverse

from charity_donation_app.models import Donation, Institution, Category
from django.db.models import Sum


class LandingPageView(View):
    """View create a main form and display it on the GET method page"""

    def get(self, request):
        total = Donation.objects.aggregate(Sum('quantity'))
        counter_institution = Donation.objects.values('institution').distinct().count()

        items = [Institution.objects.filter(type=1),
                 Institution.objects.filter(type=2),
                 Institution.objects.filter(type=3),
                 ]

        for item in items:
            if Institution.objects.filter(type=item.first().type):
                item_list = Institution.objects.filter(type=item.first().type).order_by('name')
                paginator = Paginator(item_list, 5)
                page = request.GET.get('page')
                new_item = paginator.get_page(page)
                items[items.index(item)] = new_item  # List.index() - zwraca pozycję (nr) poszczególnego elementu


        categories = Category.objects.all()
        return render(request, 'index.html', context={'total': total,
                                                      'counter_institution': counter_institution,
                                                      'items': items,
                                                      'categories': categories, })


class AddDonationView(LoginRequiredMixin, View):
    """View create a donation/add/ and display it on the GET method page"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = DonationModelForm()
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html", {"categories": categories,
                                             "institutions": institutions,
                                             "form": form})

    def post(self, request):
        form = DonationModelForm(request.POST)
        categories = request.POST['categories'].split(",")
        institution = Institution.objects.get(pk=request.POST['institution'])
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            for category in categories:
                instance.categories.add(Category.objects.get(name=category))
                instance.save()
            instance.institution = institution
            instance.save()
            return render(request, 'form-confirmation.html')
        return redirect('/form/')


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


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
    """ View created to registration user. """

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
