from sqlite3 import Timestamp
from django.db import models
from users.models import User

class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id_parent_item = models.CharField(max_length=32)
    parent_item_type = models.CharField(max_length=32)
    
    def __str__(self):
        return self.title
