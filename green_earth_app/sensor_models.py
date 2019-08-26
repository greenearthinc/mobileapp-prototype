from django.db import models

from datetime import date
import time

# User object is needed? - > login and shit -> user object extension for service account

class iotCore(models.Model):
    core_id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=40)

    def __str__(self):
        return self.name

class robot(models.Model):
    joint_id = models.CharField(max_length=20, primary_key=True)
    cluster_id = models.IntegerField()
    core = models.ForeignKey(iotCore,null=False, on_delete=models.PROTECT)

    status = models.CharField(max_length=40)

    stream_link = models.CharField(max_length=60, blank=True)

class airCluster(models.Model):
    joint_id = models.CharField(max_length=20, primary_key=True)
    cluster_id = models.IntegerField()
    core = models.ForeignKey(iotCore,null=False, on_delete=models.PROTECT)

    tvoc = models.FloatField(default=0)
    co2 = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    humidity = models.FloatField(default=0)

class lightCluster(models.Model):
    joint_id = models.CharField(max_length=20, primary_key=True)
    cluster_id = models.IntegerField()
    core = models.ForeignKey(iotCore,null=False, on_delete=models.PROTECT)

    spectrum = models.FloatField(default=0)
    state = models.CharField(max_length=10)
    status_code = models.IntegerField(default=0) # 1 is on, 0 is off, -1 is offline

class waterCluster(models.Model):
    joint_id = models.CharField(max_length=20, primary_key=True)
    cluster_id = models.IntegerField()
    core = models.ForeignKey(iotCore,null=False, on_delete=models.PROTECT)

    ph = models.FloatField(default=0)
    conductivity = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    ideal_temperature = models.FloatField(default=0)
    state = models.CharField(max_length=10)
    status_code = models.IntegerField(default=0) # 1 is on, 0 is off, -1 is offline

class channel(models.Model):
    unique_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=5)
    status = models.CharField(max_length=10, blank=True)
    light = models.ForeignKey(lightCluster,null=False, on_delete=models.PROTECT)
    water = models.ForeignKey(waterCluster,null=False, on_delete=models.PROTECT)
    air = models.ForeignKey(airCluster,null=False, on_delete=models.PROTECT)
    core = models.ForeignKey(iotCore,null=False, on_delete=models.PROTECT)

    status_code = models.IntegerField(default=0) # 0 is runnning, -1 is offline, 1 is ready to harvest, 2 is warning

    def __str__(self):
        return self.unique_id
    # x & y positions ? among other things
