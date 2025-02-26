from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #FOR CONNECT USER TO OUR MODELS WE NEED IMPORT USER IN THIS MODEL
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:                # for ordering our objects by any type of methods
        ordering = ['complete']

    
