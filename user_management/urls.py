from django.urls import path

from .views import profile_update, user_create, profile_create

app_name = 'user_management'

urlpatterns = [
    path('profile/', profile_update, name='update_profile'),
    path('register/', user_create, name='register'),
    path('profile/create/', profile_create, name='profile_create'),
]
