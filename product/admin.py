from django.contrib import admin
from .models import Product
from django.contrib.auth.admin import UserAdmin

class UserProduct(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'content', 'writer', 'write_time', 'location', 'hashtag', 'count')
    search_fields = ('title', 'category', 'writer', 'hashtag')


admin.site.register(Product)