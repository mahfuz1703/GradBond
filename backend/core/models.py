from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


job_types = (
    ('Internship', 'Internship'),
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Contract', 'Contract'),
)

# Create your models here.
class events(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    regLink = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='events', default='default_cover', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Jobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_link = models.URLField(blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=job_types, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

