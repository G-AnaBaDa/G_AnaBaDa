from django.contrib import admin
from .models import Board
# Register your models here.

class Boards(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'content', 'write_time')
    search_fields = ('user_id', 'title', 'write_time')

admin.site.register(Board)