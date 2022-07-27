"""charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from charity_donation_app.views import (
    LandingPageView,
    AddDonationView,
    LoginView,
    RegisterView,
    LogoutView,
    FormConfirmationView,
    UserProfileView,
    EditUserProfileView,
    FormSaveView,
    get_institution_by_category,
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPageView.as_view(), name='main'),
    path('donation/add/', AddDonationView.as_view(), name='add_donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('form-confirmation/', FormConfirmationView.as_view(), name='form-confirmation'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('EditProfile/', EditUserProfileView.as_view(), name='EditProfile'),
    path('save/', FormSaveView.as_view(), name='form-save'),
    path('get_institution_by_category/', get_institution_by_category, name='get_institution_by_category'),

]
