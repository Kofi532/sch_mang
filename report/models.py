from django.db import models

class reportn(models.Model): 
    stu_id = models.CharField(max_length=30,null=True, default=0)
    number = models.CharField(max_length=30,null=True, default=0)
    subjectA = models.CharField(max_length=30,null=True, default=0)
    subjectB = models.CharField(max_length=30,null=True, default=0)
    subjectC = models.CharField(max_length=30,null=True, default=0)
    subjectD = models.CharField(max_length=30,null=True, default=0)
    subjectE = models.CharField(max_length=30,null=True, default=0)
    subjectF = models.CharField(max_length=30,null=True, default=0)
    subjectG = models.CharField(max_length=30,null=True, default=0)
    subjectH = models.CharField(max_length=30,null=True, default=0)
    subjectI = models.CharField(max_length=30,null=True, default=0)
    subjectJ = models.CharField(max_length=30,null=True, default=0)
    subjectK = models.CharField(max_length=30,null=True, default=0)
    subjectL = models.CharField(max_length=30,null=True, default=0)
    school = models.CharField(max_length=30,null=True, default=0)
    level = models.CharField(max_length=30,null=True, default=0)

    def __str__(self):
        return self.subjectA

class report(models.Model): 
    stu_id = models.CharField(max_length=30,null=True, default=0)
    number = models.CharField(max_length=30,null=True, default=0)
    subjectA = models.CharField(max_length=30,null=True, default=0)
    subjectB = models.CharField(max_length=30,null=True, default=0)
    subjectC = models.CharField(max_length=30,null=True, default=0)
    subjectD = models.CharField(max_length=30,null=True, default=0)
    subjectE = models.CharField(max_length=30,null=True, default=0)
    subjectF = models.CharField(max_length=30,null=True, default=0)
    subjectG = models.CharField(max_length=30,null=True, default=0)
    subjectH = models.CharField(max_length=30,null=True, default=0)
    subjectI = models.CharField(max_length=30,null=True, default=0)
    subjectJ = models.CharField(max_length=30,null=True, default=0)
    subjectK = models.CharField(max_length=30,null=True, default=0)
    subjectL = models.CharField(max_length=30,null=True, default=0)
    school = models.CharField(max_length=30,null=True, default=0)
    level = models.CharField(max_length=30,null=True, default=0)

    def __str__(self):
        return self.subjectA

#['stu_id', 'subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL',]


class report30(models.Model): 
    stu_id = models.CharField(max_length=30,null=True, default=0)
    number = models.CharField(max_length=30,null=True, default=0)
    subjectA = models.CharField(max_length=30,null=True, default=0)
    subjectB = models.CharField(max_length=30,null=True, default=0)
    subjectC = models.CharField(max_length=30,null=True, default=0)
    subjectD = models.CharField(max_length=30,null=True, default=0)
    subjectE = models.CharField(max_length=30,null=True, default=0)
    subjectF = models.CharField(max_length=30,null=True, default=0)
    subjectG = models.CharField(max_length=30,null=True, default=0)
    subjectH = models.CharField(max_length=30,null=True, default=0)
    subjectI = models.CharField(max_length=30,null=True, default=0)
    subjectJ = models.CharField(max_length=30,null=True, default=0)
    subjectK = models.CharField(max_length=30,null=True, default=0)
    subjectL = models.CharField(max_length=30,null=True, default=0)
    school = models.CharField(max_length=30,null=True, default=0)
    level = models.CharField(max_length=30,null=True, default=0)

    def __str__(self):
        return self.subjectA

class report70(models.Model): 
    stu_id = models.CharField(max_length=30,null=True, default=0)
    number = models.CharField(max_length=30,null=True, default=0)
    subjectA = models.CharField(max_length=30,null=True, default=0)
    subjectB = models.CharField(max_length=30,null=True, default=0)
    subjectC = models.CharField(max_length=30,null=True, default=0)
    subjectD = models.CharField(max_length=30,null=True, default=0)
    subjectE = models.CharField(max_length=30,null=True, default=0)
    subjectF = models.CharField(max_length=30,null=True, default=0)
    subjectG = models.CharField(max_length=30,null=True, default=0)
    subjectH = models.CharField(max_length=30,null=True, default=0)
    subjectI = models.CharField(max_length=30,null=True, default=0)
    subjectJ = models.CharField(max_length=30,null=True, default=0)
    subjectK = models.CharField(max_length=30,null=True, default=0)
    subjectL = models.CharField(max_length=30,null=True, default=0)
    school = models.CharField(max_length=30,null=True, default=0)
    level = models.CharField(max_length=30,null=True, default=0)

    def __str__(self):
        return self.subjectA
