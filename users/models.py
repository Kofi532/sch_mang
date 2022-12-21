from django.db import models
from datetime import date

# Create your models here.
class use(models.Model):       
    username = models.CharField(max_length=10, default='')
    school = models.CharField(max_length=150,null=True)
    date = models.DateField(default=date.today())
    full_sch = models.CharField(max_length=30, default='0')
    contact_details = models.CharField(max_length=10, default='0')
    def __str__(self):
        return self.username


class sch_reg(models.Model):       
    username = models.CharField(max_length=10, default='')
    school_code = models.CharField(max_length=150,null=True)
    date = models.DateField(default=date.today())
    full_sch = models.CharField(max_length=30, default='0')
    contact_details = models.CharField(max_length=10, default='0')
    def __str__(self):
        return self.username