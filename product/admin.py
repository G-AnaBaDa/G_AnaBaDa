from django.contrib import admin
from .models import Product, Comment
class UserProduct(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'content', 'writer', 'write_time', 'location', 'hashtag', 'count')
    search_fields = ('title', 'category', 'writer', 'hashtag')

class Comments(admin.ModelAdmin):
    list_display = ('comment_id', 'user', 'content', 'created_dt', 'updated_dt')
    search_fields = ('user')

admin.site.register(Comment)
admin.site.register(Product)