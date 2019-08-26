from django.contrib.auth.models import User
from sensor_models import iotCore
from django.db import models

class coreAccess(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    core = models.OneToOneField(iotCore, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
