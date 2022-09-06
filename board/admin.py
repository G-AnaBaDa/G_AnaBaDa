from django.contrib import admin
from .models import Board
from .models import notice
class Boards(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'content', 'write_time')
    search_fields = ('user_id', 'title', 'write_time')

admin.site.register(Board)

class admin_notice(admin.ModelAdmin):
    list_display = ('title', 'content', 'write_time')
    search_fields = ('title')

admin.site.register(notice)