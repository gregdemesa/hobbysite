from django import forms

from .models import Commission, Job, JobApplication
from django.core.validators import MinValueValidator


class CommissionForm(forms.ModelForm):
    role = forms.CharField(max_length=100)
    manpower_required = forms.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Commission
        # Fields from Commission model
        fields = ['title', 'description', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        # 'applicant' is automatically set to the logged-in user
        fields = ['job', 'status']

    def __init__(self, *args, **kwargs):
        super(JobApplicationForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 'Pending'  # Initial status
