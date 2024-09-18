from django.contrib import admin
from .models import Profile, Project, WorkExperience, Education, Certification

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'profile']

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'profile']

class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'profile']

class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'profile']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Certification, CertificationAdmin)
