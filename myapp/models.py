from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.
class Chat(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE, # quando a sessão for apagada, apaga as mensagens
    )
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
