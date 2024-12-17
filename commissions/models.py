from django.db import models
from django.urls import reverse

from user_management.models import Profile


class Commission(models.Model):
    STATUS_CHOICES = (
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued')
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission', args=[self.pk])

    class Meta:
        ordering = ['created_on']


class Job(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Full', 'Full')
    )
    commission = models.ForeignKey(Commission,
                                   on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Open')

    class Meta:
        ordering = ['-status', '-manpower_required', 'role']


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-status', '-applied_on']
