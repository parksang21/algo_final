from django.contrib import admin

from .models import StudentModel, StudentInstance

# Register your models here.

admin.site.register(StudentModel)

@admin.register(StudentInstance)
class StudentInstanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'attend_time', 'status']
