from django.contrib import admin
from .models import DwUser, Subscription, RefferalSystem, Statistics

class DwUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('username',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_dur', 'start_date', 'expiration_date', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('sub_dur', 'start_date', 'expiration_date')
    ordering = ('expiration_date',)
    date_hierarchy = 'start_date'

# Настройка модели RefferalSystem в админке
class RefferalSystemAdmin(admin.ModelAdmin):
    list_display = ('user', 'refferal_available', 'code', 'refferal_number', 'refferal_bonus')
    search_fields = ('user__username', 'user__email', 'code')
    list_filter = ('refferal_available',)
    ordering = ('user',)

# Настройка модели Statistics в админке
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'reg_date', 'last_launch', 'launch_number', 'display_playtime_in_minutes')
    search_fields = ('user__username', 'user__email')
    list_filter = ('reg_date', 'last_launch')
    ordering = ('-reg_date',)
    readonly_fields = ('display_playtime_in_minutes',)
    list_display_links = ('user',)

admin.site.register(DwUser, DwUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin) 
admin.site.register(RefferalSystem, RefferalSystemAdmin) 
admin.site.register(Statistics, StatisticsAdmin)

