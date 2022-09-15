from django.db import models
from account.models import User

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(default='', null=False, blank=False, max_length=50)
    category = models.CharField(default='', null=False, blank=False, max_length=10)
    content = models.TextField(default='', null=False, blank=False)
    writer = models.ForeignKey('account.User', on_delete=models.CASCADE, default=User.objects.first().pk)
    write_time = models.DateField(auto_now=True)
    location = models.CharField(default='', null=False, blank=False, max_length=10)
    hashtag = models.CharField(default='', null=True, blank=True, max_length=10)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title