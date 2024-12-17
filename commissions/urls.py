from django.urls import path

from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView

urlpatterns = [
    path('commissions/list/', CommissionListView.as_view(), name="commissions"),
    path('commissions/detail/<int:pk>/',
         CommissionDetailView.as_view(), name="commission"),
    path('commissions/add/', CommissionCreateView.as_view(), name="commission_add"),
    path('commissions/<int:pk>/edit/',
         CommissionUpdateView.as_view(), name="commission_edit")
]

app_name = "commissions"
