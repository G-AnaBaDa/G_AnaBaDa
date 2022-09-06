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