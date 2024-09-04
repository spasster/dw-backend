from django.contrib import admin
from .models import  Subscription, SubscriptionKey
from django import forms
from django.contrib import messages
from .enums import Sub

# Форма для генерации ключей
class GenerateKeysForm(forms.Form):
    sub_dur = forms.ChoiceField(choices=Sub.get_choices(), label="Тип подписки")
    count = forms.IntegerField(min_value=1, max_value=100, label="Количество ключей")

class SubscriptionKeysAdmin(admin.ModelAdmin):
    list_display = ('key', 'sub_dur', 'created_at', 'expires_at')
    actions = ['generate_keys_action']

    def generate_keys_action(self, request, queryset):
        if 'apply' in request.POST:
            form = GenerateKeysForm(request.POST)
            if form.is_valid():
                count = form.cleaned_data['count']
                sub_dur = form.cleaned_data['sub_dur']

                keys = []
                for _ in range(count):
                    key = SubscriptionKey.generate_key()
                    keys.append(SubscriptionKey(key=key, sub_dur=sub_dur))
                SubscriptionKey.objects.bulk_create(keys)

                self.message_user(request, f"Успешно создано {count} ключей.", level=messages.SUCCESS)
                return

        else:
            form = GenerateKeysForm(initial={'sub_dur': Sub.MONTH.name})

        # Здесь мы рендерим стандартную страницу с формой для подтверждения действия
        return self.render_generate_keys_form(request, form)

    def render_generate_keys_form(self, request, form):
        context = {
            'title': 'Сгенерировать ключи',
            'form': form,
            'opts': self.model._meta,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
            'media': self.media,
        }
        return admin.helpers.render_action_form(
            request,
            context,
            admin.helpers.ACTION_FORM_TEMPLATE,
        )

    generate_keys_action.short_description = "Сгенерировать ключи"

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_dur', 'start_date', 'expiration_date', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('sub_dur', 'start_date', 'expiration_date')
    ordering = ('expiration_date',)
    date_hierarchy = 'start_date'

    
admin.site.register(Subscription, SubscriptionAdmin) 
admin.site.register(SubscriptionKey, SubscriptionKeysAdmin) 
