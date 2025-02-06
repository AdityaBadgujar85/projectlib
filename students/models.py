from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100,null=True)
    ofclass = models.CharField(max_length=100,null=True)
    division = models.CharField(max_length=100,null=True)
    branch = models.CharField(max_length=100,null=True)
    title = models.CharField(max_length=100,null=True)
    discription = models.CharField(max_length=100,null=True)
    video = models.FileField(upload_to='Video/',null=True)
    thumbnail = models.FileField(upload_to='Thumbnail/',null=True)
    academic_year = models.CharField(max_length=100,null=True)
    date = models.DateField(null=True)
    domain = models.CharField(max_length=100,null=True)
    Achievements = models.CharField(max_length=100,null=True)
    LevelofProject = models.CharField(max_length=100,null=True)
    Challenges = models.CharField(max_length=100,null=True)

def __str__(self):
     return self.title
    