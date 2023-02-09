from django.db import models
from django.core.files.storage import FileSystemStorage


# Create your models here.
class student(models.Model):
    course_name = models.CharField(max_length=50)
    course_id = models.CharField(max_length=50)
    attempted_id=models.CharField(max_length=50)
    cand_name=models.CharField(max_length=50)
    cand_email=models.CharField(max_length=50)
    marks=models.IntegerField()
    grade=models.CharField(max_length=3)

class retrieve_file(models.Model):
    def upload(self,name,content):
        myfile=FileSystemStorage()
        name=myfile.save(name,content)
        return myfile.url(name)

class dashboard(models.Model):
    cand_name=models.CharField(max_length=50)
    progress_score=models.IntegerField()
    # checkbox=models.BooleanField(default=False)

