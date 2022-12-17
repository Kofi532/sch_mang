from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.

class fees_update(models.Model):       
    stu_id = models.CharField(max_length=10, default='')
    firstname = models.CharField(max_length=150,null=True)
    middlename = models.CharField(max_length=100,null=True)    
    lastname = models.CharField(max_length=100,null=True)
    level = models.CharField(max_length=10,null=True)
    amount = models.FloatField(max_length=12, default='',null=True)
    fee = models.FloatField(max_length=12, default='',null=True)
    balance = models.FloatField(max_length=12, default='',null=True)
    school = models.CharField(max_length=12, default='',null=True)
    datey = models.DateField(max_length=40, default= date.today(),null=True)
    def __str__(self):
        return self.stu_id

#['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'datey']