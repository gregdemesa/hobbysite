from django.contrib import admin

from .models import Commission, Job, JobApplication


class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on', 'author')
    search_fields = ('title', 'status', 'author__username')
    list_filter = ('status', 'created_on', 'updated_on')
    readonly_fields = ('created_on', 'updated_on', 'author')


class JobInLine(admin.TabularInline):
    model = Job


class JobAdmin(admin.ModelAdmin):
    model = Job


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
