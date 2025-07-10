from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.
class Chat(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Conf(models.Model):
    mcp_path = models.CharField(max_length=500)
    ollama_model = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj