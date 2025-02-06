from django.contrib import admin
from students.models import Student

class Student_Info(admin.ModelAdmin):
    list_display = ('name','ofclass','division','branch','title','discription','video','thumbnail','academic_year','date','domain','Achievements','LevelofProject','Challenges')

admin.site.register(Student,Student_Info)
# Register your models here.

