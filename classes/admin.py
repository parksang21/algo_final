from django.contrib import admin
from .models import ClassModel,RegisterModel
# Register your models here.


@admin.register(ClassModel)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_code', 'credit', 'major']

@admin.register(RegisterModel)
class RegisterAdmin(admin.ModelAdmin):
    list_distplay = ['prof', 'class_model', 'division']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('student')