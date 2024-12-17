from django.db import models
from django.urls import reverse
from django.utils import timezone
from user_management.models import Profile
# Create your models here.


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('merchstore:product_type', args=[self.pk])

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )
    description = models.TextField()
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
    )
    price = models.DecimalField(max_digits=100, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    STATUS_CHOICES = (
        ("AVAILABLE", "Available"),
        ("ON SALE", "On Sale"),
        ("OUT OF STOCK", "Out of Stock"),
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('merchstore:product', args=[self.pk])

    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    buyer = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL,
        related_name='transactions',
        default=None
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )
    amount = models.PositiveIntegerField(default=0)

    STATUS_CHOICES = (
        ("ON CART", "On Cart"),
        ("TO PAY", "To Pay"),
        ("TO SHIP", "To Ship"),
        ("TO RECEIVE", "To Receive"),
        ("DELIVERED", "Delivered")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ON CART'
    )
    created_on = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} piece/s"
