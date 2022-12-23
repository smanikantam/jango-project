from django.db import models
from django.core.files.storage import FileSystemStorage


# Create your models here.
class student(models.Model):
    
    # first_name=models.CharField(max_length=50)
    # last_name=models.CharField(max_length=50)
	# username=models.CharField(max_length=50)
	# email=models.CharField(max_length=50)
	# password=models.CharField(max_length=50)
	# conform_password=models.CharField(max_length=50)



    course_name = models.CharField(max_length=50)
    course_id = models.CharField(max_length=50)
    attempted_id=models.IntegerField()
    cand_name=models.CharField(max_length=50)
    cand_email=models.CharField(max_length=50)
    marks=models.IntegerField()
    grade=models.CharField(max_length=3)

class retrieve_file(models.Model):
    def upload(self,name,content):
        myfile=FileSystemStorage()
        name=myfile.save(name,content)
        return myfile.url(name)

