from django.db import models
from account.models import User


class Board(models.Model): #발상의 전환
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE, default=User.objects.first().pk)
    title = models.CharField(default='', null=False, blank=False, max_length=50)
    content = models.TextField(default='', null=False, blank=False)
    write_time = models.DateField(auto_now_add=True)

    def str(self):
        return self.title


