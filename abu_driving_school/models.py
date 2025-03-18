from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    comment = models.TextField()  # The review text
    rating = models.IntegerField()  # Rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"


class NewModel(models.Model):
    name = models.CharField(max_length=100)
