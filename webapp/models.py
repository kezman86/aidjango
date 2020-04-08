from django.db import models

# Create your models here.
class Case(models.Model):
    caseID = models.CharField(max_length = 18)
    caseNumber = models.CharField(max_length = 18)
    caseSubject = models.CharField(max_length = 1024)
    caseDescription=models.TextField(max_length = 10240, default = "")
    caseModule = models.CharField(max_length = 64)
    published = models.IntegerField(default = 0)