from django.db import models

# Create your models here.
class Student(models.Model):
    
    roll = models.IntegerField(primary_key=True)
    s_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    marks = models.FloatField()
    
    def __str__(self):
        return self.s_name
