from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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

