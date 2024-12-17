from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Assuming these are the fields you want to update
        fields = ['display_name', 'email_address']


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    display_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['display_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        display_name = self.cleaned_data.get('display_name')
        if display_name:
            if User.objects.filter(username=display_name).exists():
                raise forms.ValidationError(
                    "Username already exists. Please choose a different one.")
            else:
                user.username = display_name
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user, display_name=display_name)
        return user
