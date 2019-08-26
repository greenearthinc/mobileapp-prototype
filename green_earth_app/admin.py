# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sensor_models import iotCore
from sensor_models import airCluster, waterCluster, lightCluster, robot, channel
from user_models import serviceAccount, workerAccount
from access_models import coreAccess
from support_files import generate_key

import random
# Register your models here.

from django.contrib.auth.models import User
from support_files import publish_information

def create_service_token(modeladmin, request, queryset):
    for q in queryset:
        username = "core_id_"+str(q.core_id)
        try:
            user= User.objects.get(username=username)
        except:
            key = generate_key()
            user = User.objects.create_user(username, '', key)
            user.save()
            new_account = serviceAccount()
            new_account.user = user
            new_account.access_token = key
            new_account.save()

def run_nutrient_motors(modeladmin, request, queryset):
    publish_information("water_nutr", 0, 1) # 0 is empty value

def simulate_farms(modeladmin, request, queryset):
    for q in queryset:
        id = q.core_id
        channel.objects.filter(core=q).delete()
        waterCluster.objects.filter(core=q).delete()
        airCluster.objects.filter(core=q).delete()
        lightCluster.objects.filter(core=q).delete()
        robot.objects.filter(core=q).delete()
        letter_combo = ["A", "B", "C", "D", "E", "F", "G", "H"]
        unique_value = 1
        air = airCluster()
        air.joint_id = str(q.core_id) + "-" + str(1)
        air.core = q
        air.cluster_id = 1
        air.humidity = 50
        air.temperature = 26.0
        air.tvoc = 200
        air.co2 = 10
        air.pessure = 101.3
        air.save()

        i =0
        while i < len(letter_combo):
            j = 1
            while j <= 8:
                name  = letter_combo[i] + str(j)
                new_channel = channel()
                new_channel.name = name
                new_channel.unique_id = str(q.core_id) + "-" + name
                new_channel.core = q
                water = waterCluster()
                water.joint_id = str(q.core_id) + "-" + str(unique_value)
                water.core = q
                water.cluster_id = str(unique_value)
                water.temperature = 25.0
                water.conductivity = 0.6
                water.ph = 7
                v = int(random.random()*10)
                if v > 7:
                    water.status_code = 1
                water.save()
                light = lightCluster()
                light.joint_id = str(q.core_id) + "-" + str(unique_value)
                light.core = q
                light.cluster_id = str(unique_value)
                v = int(random.random()*10)
                if v < 7:
                    light.status_code = 1
                    light.state = "ON"
                else:
                    light.state = "OFF"
                    light.status_code = 0
                light.spectrum = 590
                light.save()
                j += 1
                unique_value += 1
                new_channel.water = water
                new_channel.light = light
                new_channel.air = air
                new_channel.save()
            i += 1

        cluster = robot()
        cluster.joint_id = str(q.core_id) + "-" + str(1)
        cluster.core = q
        cluster.cluster_id = 1
        cluster.status = "Inspecting B6"
        cluster.save()





@admin.register(channel)
class adminChannel(admin.ModelAdmin):
    pass

@admin.register(iotCore)
class adminIotCore(admin.ModelAdmin):
    actions = [create_service_token, simulate_farms, run_nutrient_motors]

@admin.register(airCluster)
class adminAirCluster(admin.ModelAdmin):
    pass

@admin.register(waterCluster)
class adminWaterCluster(admin.ModelAdmin):
    pass

@admin.register(lightCluster)
class adminLightCluster(admin.ModelAdmin):
    pass

@admin.register(robot)
class adminRobot(admin.ModelAdmin):
    pass

@admin.register(serviceAccount)
class adminServiceAccount(admin.ModelAdmin):
    pass

@admin.register(workerAccount)
class adminWorkerAccount(admin.ModelAdmin):
    pass

@admin.register(coreAccess)
class adminCoreAccess(admin.ModelAdmin):
    pass