from django.contrib import admin
from .models import DwUser


class DwUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('username',)

admin.site.register(DwUser, DwUserAdmin)
