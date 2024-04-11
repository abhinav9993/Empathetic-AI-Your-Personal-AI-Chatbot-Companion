from django.db import models

from django.db import models
from django.conf import settings

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_user_message = models.BooleanField(default=True)  # True for user messages, False for bot responses

    def __str__(self):
        return self.text[:50]  # Display the first 50 characters of the message

