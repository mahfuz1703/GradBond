from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import alumniProfile, studentProfile
from core.models import events, Jobs

# Register your models here.
class AlumniResources(resources.ModelResource):
    class Meta:
        model = alumniProfile
        fields = ('id', 'user__email', 'full_name', 'university', 'dept', 'student_id', 'graduation_year', 'company', 'job_title', 'graduation_year', 'linkedin', 'image')
class AlumniProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'university', 'dept', 'company', 'job_title', 'total_events', 'total_jobs')
    search_fields = ('full_name', 'university', 'dept', 'company', 'job_title')
    list_filter = ('university', 'dept', 'company', 'job_title')
    resources_class = AlumniResources

    def total_events(self, obj):
        return events.objects.filter(user=obj.user).count()
    total_events.short_description = 'Total Events'

    def total_jobs(self, obj):
        return Jobs.objects.filter(user=obj.user).count()
    total_jobs.short_description = 'Total Jobs'
    
admin.site.register(alumniProfile, AlumniProfileAdmin)


class StudentResources(resources.ModelResource):
    class Meta:
        model = studentProfile
        fields = ('id', 'user__email', 'full_name', 'university', 'dept', 'student_id', 'image')

class StudentProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'university', 'dept', 'student_id')
    search_fields = ('full_name', 'university', 'dept', 'student_id')
    list_filter = ('university', 'dept')

    resources_class = StudentResources

admin.site.register(studentProfile, StudentProfileAdmin)
