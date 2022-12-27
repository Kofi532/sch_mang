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
    amount = models.FloatField(max_length=12, default=0,null=True)
    amountpaid_term1 = models.FloatField(max_length=12, default=0,null=True)
    amountpaid_term2 = models.FloatField(max_length=12, default=0,null=True)
    amountpaid_term3 = models.FloatField(max_length=12, default=0,null=True)
    fee = models.FloatField(max_length=12, default=0,null=True)
    balance = models.FloatField(max_length=12, default=0,null=True)
    school = models.CharField(max_length=12, default='',null=True)
    datey = models.DateField(max_length=40, default= date.today(),null=True)
    school_full = models.CharField(max_length=30, default='',null=True)
    mother_name = models.CharField(max_length=30, default='None',null=True)
    mother_contact = models.CharField(max_length=30, default='None',null=True)
    father_name = models.CharField(max_length=30, default='None',null=True)
    father_contact = models.CharField(max_length=30, default='None',null=True)
    def __str__(self):
        return self.stu_id

#['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
