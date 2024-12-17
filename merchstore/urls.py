from .views import CartView, TransactionListView, ProductCreateView, ProductUpdateView, ProductListView, ProductDetailView
from django.urls import path

urlpatterns = [
    path('items', ProductListView.as_view(), name="product_type"),
    path('item/<int:pk>', ProductDetailView.as_view(), name="product"),
    path('item/add', ProductCreateView.as_view(), name='product_create'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='product_update'),
    path('cart', CartView.as_view(), name='cart'),
    path('transactions', TransactionListView.as_view(), name='transaction')
]

app_name = "merchstore"
