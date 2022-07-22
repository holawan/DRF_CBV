from django.db import models
from authentication.models import User

# Create your models here.


from helpers.models import TrackingModel


class Todo(TrackingModel) :
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.title