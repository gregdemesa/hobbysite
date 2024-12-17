from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm

def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/profile')  # Redirect to profile view after successful update
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})
