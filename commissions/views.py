from django.shortcuts import render, redirect, get_object_or_404
from .models import Commission, Job, JobApplication
from django.views import View
from typing import Any
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from user_management.models import Profile
from .models import Commission, JobApplication, Job
from .forms import CommissionForm


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissionList.html'

    def get_queryset(self):
        queryset = Commission.objects.all().order_by('status', '-created_on')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user

            # Filter commissions where the current user is the author

            my_posted_commissions = Commission.objects.filter(
                author=user.profile).order_by('status', '-created_on')
            context['my_posted_commissions'] = my_posted_commissions

            # Filter commissions where the current user has applied
            my_applied_commissions = Commission.objects.filter(
                job__jobapplication__applicant=user.profile).order_by('status', '-created_on').distinct()
            context['my_applied_commissions'] = my_applied_commissions

            all_commissions = Commission.objects.all()
            context['all_commissions'] = all_commissions
        return context

    def post(self, request, *args, **kwargs):
        form = CommissionForm(request.POST)
        if form.is_valid():
            form.save()
            return self.get(request, *args, **kwargs)
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class CommissionDetailView(LoginRequiredMixin, DetailView):
    model = Commission
    template_name = 'commission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        jobs = Job.objects.filter(commission=commission)

        # Calculate total manpower required
        total_manpower_required = jobs.aggregate(
            total_manpower=Sum('manpower_required'))['total_manpower'] or 0

        # Calculate total signees for all jobs
        total_signees = JobApplication.objects.filter(
            job__in=jobs, status='Accepted').count()

        # Calculate remaining open manpower
        remaining_manpower = total_manpower_required - total_signees

        # Determine if the "Apply to Job" button should be clickable for each job
        can_apply = {}
        for job in jobs:
            can_apply[job.pk] = total_signees < job.manpower_required
        is_owner = commission.author == self.request.user.profile

        context['is_owner'] = is_owner
        context['commission'] = commission
        context['jobs'] = jobs
        context['total_manpower_required'] = total_manpower_required
        context['total_signees'] = total_signees
        context['remaining_manpower'] = remaining_manpower
        context['can_apply'] = can_apply

        # Include the updated commission instance in the context
        context['commission'] = self.object

        return context

    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, pk=job_id)
        accepted_applicants_count = job.jobapplication_set.filter(
            status='Accepted').count()
        if accepted_applicants_count < job.manpower_required + 1:
            # Create a JobApplication object
            JobApplication.objects.create(
                job=job, applicant=request.user.profile, status='Pending')
            # increment the number of applicants
            job.jobapplication_set.create(
                applicant=request.user.profile, status='Accepted')
            return redirect('commissions:commission', pk=self.kwargs['pk'])
        else:
            # Handle the case where the job cannot be applied
            pass


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'createCommission.html'

    success_url = reverse_lazy('commissions:commissions')

    def form_valid(self, form):
        commission = form.save(commit=False)
        commission.author = self.request.user.profile
        commission.save()
        job = commission.job_set.create(
            role=form.cleaned_data['role'],
            manpower_required=form.cleaned_data['manpower_required']
        )

        return super().form_valid(form)


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = "updateCommission.html"

    def get_success_url(self):
        return reverse_lazy('commissions:commission', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        manpower_required = form.cleaned_data.get('manpower_required')
        role = form.cleaned_data.get('role')

        job = self.object.job_set.first()
        if job:
            job.manpower_required = manpower_required
            job.role = role
            job.save()

        return super().form_valid(form)
