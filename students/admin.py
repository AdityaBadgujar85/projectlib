from django.contrib import admin
from students.models import Student

class Student_Info(admin.ModelAdmin):
    list_display = ('name','ofclass','division','branch','title','discription','video','thumbnail','academic_year','date','domain','Achievements','LevelofProject','Challenges')

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'  # Display name for the column
admin.site.register(Student,Student_Info)
# Register your models here.

