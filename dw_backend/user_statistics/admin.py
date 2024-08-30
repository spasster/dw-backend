from django.contrib import admin
from .models import  RefferalSystem, Statistics

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'reg_date', 'last_launch', 'launch_number', 'display_playtime_in_minutes')
    search_fields = ('user__username', 'user__email')
    list_filter = ('reg_date', 'last_launch')
    ordering = ('-reg_date',)
    readonly_fields = ('display_playtime_in_minutes',)
    list_display_links = ('user',)

class RefferalSystemAdmin(admin.ModelAdmin):
    list_display = ('user', 'refferal_available', 'code', 'refferal_number', 'refferal_bonus')
    search_fields = ('user__username', 'user__email', 'code')
    list_filter = ('refferal_available',)
    ordering = ('user',)

admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(RefferalSystem, RefferalSystemAdmin) 


