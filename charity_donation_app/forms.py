from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """
        A form that creates a user, with no privileges, from the given username and
        password.
    """

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'Imię'}),
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

    login = forms.CharField(label="Email")
    password = forms.CharField(label="Insert password", widget=forms.PasswordInput)
