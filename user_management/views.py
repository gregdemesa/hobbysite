from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from collections import defaultdict

from .forms import ProfileForm, CreateProfileForm, UserRegistrationForm
from commissions.models import Commission
from merchstore.models import Product, Transaction


@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', {'form': form})


def profile_create(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    else:
        form = CreateProfileForm()
    return render(request, 'profile_create.html', {'form': form})


def user_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/homepage')
            except forms.ValidationError as e:
                form.add_error(None, e)  # Add form-wide error
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
