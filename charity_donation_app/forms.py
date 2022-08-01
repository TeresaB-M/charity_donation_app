from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from charity_donation_app.models import Donation


class RegisterForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given username and
        password.
    """

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':
                                'potwierdź hasło'}),)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={'placeholder': 'email'}),
            "last_name": forms.TextInput(attrs={'placeholder': 'nazwisko'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'imię'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """ Create login form"""

    login = forms.CharField(label="email", widget=forms.PasswordInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(label="hasło", widget=forms.PasswordInput(attrs={'placeholder': 'hasło'}))


class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['quantity', 'street', 'house_number', 'phone_number', 'city', 'zip_code', 'pick_up_date',
                  'pick_up_time', 'pick_up_comment']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': 'Hasło'})
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = "Aby potwierdzić podaj hasło"
        self.fields["first_name"].label = "Zmień imię:"
        self.fields["last_name"].label = "Zmień nazwisko:"
        self.fields["email"].label = "Zmień email:"


class MyUserCreation(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name')


class EditDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['pick_up_date']
