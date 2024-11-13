from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class alumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    email = models.EmailField()
    graduation_year = models.IntegerField()
    company = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    linkedin = models.URLField()

    def __str__(self):
        return self.user.first_name

class studentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.user.first_name
