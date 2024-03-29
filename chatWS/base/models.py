from django.db import models
from django.contrib.auth.models import User

class Friends(models.Model):
    username = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username

class BaseMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message
    
