from django.db import models
from datetime import date

# Create your models here.
class use(models.Model):       
    username = models.CharField(max_length=10, default='')
    school = models.CharField(max_length=150,null=True)
    date = models.DateField(default=date.today())
    def __str__(self):
        return self.username
