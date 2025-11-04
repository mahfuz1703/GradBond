from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from core.models import University

# Create your models here.
class alumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    dept = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    image = CloudinaryField('image', folder='alumni', default='default_alumni', blank=True, null=True)
    contributions_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name = 'Alumni Profile'
        verbose_name_plural = 'Alumni Profiles'

class studentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True)
    dept = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image = CloudinaryField('image', folder='students', default='default_ayh3h7', blank=True, null=True)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
