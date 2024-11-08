from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Event(models.Model):
    name=models.CharField(max_length=200)
    image=models.FileField(upload_to='event/images')
    description=models.TextField()
    def is_booked_by_user(self, user):
        # Check if the current user has booked this event
        return BookEvent.objects.filter(event=self, user=user).exists()
    def __str__(self):
        return self.name
class BookEvent(models.Model):
    name=models.CharField(max_length=200)  
    email=models.EmailField()
    phone=models.IntegerField()
    description=models.TextField()
    date=models.DateField()
    place=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    event=models.ForeignKey( Event,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.name
class Enquiery(models.Model):
    name=models.CharField(max_length=200)  
    email=models.EmailField()
    event=models.CharField(max_length=200,default="wed")
    phone=models.IntegerField()
    description=models.TextField()
    timestamp = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.name
    
class MainImage(models.Model):
    image=models.FileField(upload_to='events/images')
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class SubImage(models.Model):
    images = models.ForeignKey(MainImage, on_delete=models.CASCADE)
    image=models.FileField(upload_to='sub/images')
    
    
    
    
    
    
    