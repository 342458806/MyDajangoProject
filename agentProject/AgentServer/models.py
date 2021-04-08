from django.db import models


# Create your models here.
class Post(models.Model):
    headline = models.CharField(max_length=50, verbose_name='headline',)
    category = models.CharField(max_length=10, verbose_name='category',)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    region = models.CharField(max_length=10, verbose_name='region')
    details = models.CharField(max_length=50, verbose_name='details')
    date = models.CharField(max_length=20, verbose_name='date')

    def __str__(self):
        return self.headline
