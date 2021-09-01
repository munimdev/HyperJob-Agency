from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField, ForeignKey


# Create your models here.
class Resume(models.Model):
    description = CharField(max_length=1024)
    author = ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'resume'
