from django.contrib import admin

from .models import DateModel

@admin.register(DateModel)
class DateAdmin(admin.ModelAdmin):
    list_display = ['register', 'today', 'start_time']
