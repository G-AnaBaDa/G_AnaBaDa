from django.db import models
from account.models import User


class Board(models.Model):
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE, default=User.objects.first().pk)
    title = models.CharField(default='', null=False, blank=False, max_length=50)
    content = models.TextField(default='', null=False, blank=False)
    write_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class notice(models.Model):
    title = title = models.CharField(default='', null=False, blank=False, max_length=50)
    content = models.TextField(default='', null=False, blank=False)
    write_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    board = models.ForeignKey('board.Board', on_delete=models.CASCADE, null=True, related_name='board_comments')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True,related_name='board_comment_user')
    content = models.CharField(default='',null=True,max_length=200)
    created_dt = models.DateField(auto_now_add=True)
    updated_dt = models.DateField(auto_now=True)

    def __str__(self):
        return self.content