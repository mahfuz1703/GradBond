from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import events, Jobs, University

# Events model resources for import/export functionality
class EventsResources(resources.ModelResource):
    class Meta:
        model = events
        fields = ('id', 'user__email', 'title', 'description', 'date', 'time', 'regLink', 'location', 'image')

class EventsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'time', 'location')
    search_fields = ('user__email', 'title', 'location')
    list_filter = ('date', 'location')
    resource_class = EventsResources
admin.site.register(events, EventsAdmin)


# Jobs model resources for import/export functionality
class JobsResources(resources.ModelResource):
    class Meta:
        model = Jobs
        fields = ('id', 'user__email', 'title', 'company', 'job_link', 'job_type', 'experience', 'salary', 'description', 'deadline')

class JobsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'title', 'company', 'job_type', 'salary', 'deadline')
    search_fields = ('user__email', 'title', 'company', 'job_type', 'salary')
    list_filter = ('job_type', 'deadline')
    resource_class = JobsResources

admin.site.register(Jobs, JobsAdmin)

# University model resources for import/export functionality
class UniversityResources(resources.ModelResource):
    class Meta:
        model = University
        fields = ('id', 'name', 'short_name', 'location', 'website')

class UniversityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'short_name', 'location', 'website')
    search_fields = ('name', 'short_name', 'location')
    resource_class = UniversityResources
admin.site.register(University, UniversityAdmin)
