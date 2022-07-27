from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, DonationModelForm, EditProfileForm, MyUserCreation, EditDonationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from charity_donation_app.models import Donation, Institution, Category
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist


class LandingPageView(View):
    """View create a main form and display it on the GET method page"""

    def get(self, request):
        total = Donation.objects.aggregate(Sum('quantity'))
        counter_institution = Donation.objects.values('institution').distinct().count()
        categories = Category.objects.all()

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
        category = Category.objects.all()
        institution = Institution.objects.all()

        return render(request, 'form.html', {
            'category': category,
            'institution': institution,
            'form': form,
        })


@login_required(login_url='/login/')
def get_institution_by_category(request):
    cat_id = request.GET.getlist('cat_id')
    if cat_id is not None:
        categories = Category.objects.filter(pk__in=cat_id)
        institutions = Institution.objects.filter(categories__in=cat_id).distinct()
    else:
        institutions = Institution.objects.all()

    return render(request, "api_institution.html", {'institutions': institutions,
                                                    'cat_id': cat_id,
                                                    'form': MyUserCreation, })


class FormSaveView(LoginRequiredMixin, View):

    def post(self, request):
        categories = request.POST.get('categories')
        quantity = request.POST.get('bags')
        institution = request.POST.get('organization')
        try:
            organization = Institution.objects.get(id=institution)
            category = Category.objects.get(id=categories)
        except ObjectDoesNotExist:
            organization = None
            category = None
        else:
            street = request.POST.get('street')
            house_number = request.POST.get('house_number')
            city = request.POST.get('city')
            post = request.POST.get('postcode')
            phone = request.POST.get('phone')
            data = request.POST.get('data')
            time = request.POST.get('time')
            comments = request.POST.get('more_info')
            user = request.user.id
            email = request.user.email
            donation = Donation.objects.create(quantity=quantity,
                                               institution_id=institution,
                                               street=street,
                                               house_number=house_number,
                                               city=city,
                                               zip_code=post,
                                               phone_number=phone,
                                               pick_up_date=data,
                                               pick_up_time=time,
                                               pick_up_comment=comments,
                                               user_id=user,
                                               )
            donation.categories.set(categories)
            donation.save()
            return render(request, 'form-save.html', {'quantity': quantity,
                                                      'institution': institution,
                                                      'street': street,
                                                      'house_number': house_number,
                                                      'city': city,
                                                      'post': post,
                                                      'phone': phone,
                                                      'data': data,
                                                      'time': time,
                                                      'comments': comments,
                                                      'organization': organization,
                                                      'category': category, })

        return redirect('/form-confirmation/')


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


class UserProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        donations = Donation.objects.filter(user_id=request.user.id).order_by('is_taken')
        return render(request, 'profile.html', context={"user": request.user,
                                                        "donations": donations, })


class EditUserProfileView(View):
    def get(self, request):
        form = EditProfileForm(initial={"first_name": request.user.first_name,
                                        "last_name": request.user.last_name,
                                        "email": request.user.email})
        return render(request, 'edit_profile.html', context={"form": form})

    def post(self, request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.email, password=form.cleaned_data["password"])
            if user is not None:
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.save()
                return redirect(reverse('profile'))
            else:
                form = EditProfileForm(initial={"first_name": form.cleaned_data["first_name"],
                                                "last_name": form.cleaned_data["last_name"],
                                                "email": form.cleaned_data["email"]})
                message = "Podano błędne hasło!"
                return render(request, "edit_profile.html", context={"form": form,
                                                                     "message": message})
        return render(request, 'edit_profile.html', context={"form": form})


class EditDonation(View):
    def get(self, request, donation_id):
        donation = Donation.objects.get(pk=donation_id)
        form = EditDonationForm(instance=donation)
        return render(request, 'edit_donation.html', {'form': form})

    def post(self, request, donation_id):
        donation = Donation.objects.get(pk=donation_id)
        form = EditDonationForm(request.POST)
        if form.is_valid():
            pick_up_date = form.cleaned_data['pick_up_date']
            donation.pick_up_date = pick_up_date
            donation.is_taken = 1
            donation.save()
            return redirect('profile')
        return render(request, 'edit_donation.html', {'form': form})