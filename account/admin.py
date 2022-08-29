from django.contrib import admin
from .models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'email', 'name', 'nickname', 'name', 'phone_number')
    search_fields = ('account_id', 'email', 'name', 'nickname', 'name', 'phone_number')


admin.site.register(User, AccountAdmin)