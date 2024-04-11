from django.contrib import admin
from .models import Message
from .utils import encode_id, decode_id
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'is_user_message')
    list_filter = ('created_at', 'is_user_message')
    search_fields = ('text',)


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('encoded_id', 'username', 'email', 'is_staff')

    def encoded_id(self, obj):
        return mark_safe(f'<span title="{obj.id}">{encode_id(obj.id)}</span>')
    encoded_id.short_description = 'ID'

    # If you want to make the encoded ID searchable, you'll need to override get_search_results
    def get_search_results(self, request, queryset, search_term):
        # Check if the search_term is encoded ID and decode it
        try:
            decoded_id = decode_id(search_term)
            return super().get_search_results(request, queryset, str(decoded_id))
        except Exception:
            # If decoding fails, just use the original search term
            return super().get_search_results(request, queryset, search_term)