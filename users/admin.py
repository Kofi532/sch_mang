from django.contrib import admin
from .models import use, sch_reg, act, class_fee
# Register your models here.
admin.site.register(use)
admin.site.register(sch_reg)
admin.site.register(act)
admin.site.register(class_fee)