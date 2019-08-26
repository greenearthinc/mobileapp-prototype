
from django.contrib.auth.models import User
from django.db import models


class serviceAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class workerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username