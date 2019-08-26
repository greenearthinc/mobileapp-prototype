import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from sensor_models import waterCluster, airCluster, lightCluster, robot, iotCore, channel
from access_models import coreAccess
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.conf import settings

from user_models import workerAccount
from support_files import compare_match, generate_key

from support_files import publish_information

@csrf_exempt
def web_app_router(request):
    if compare_match(request.path,"/web_app/login/"):
        return login(request)
    access_token = request.META.get("HTTP_ACCESS_TOKEN")
    if access_token is None:
        rdict = {"Error": "No access-token header"}
        return JsonResponse(rdict, status=400)
    verification, user = verify_access_token(access_token)
    if compare_match(request.path,"/web_app/verify_token/"):
        return verify_token(request, verification)
    if verification == False:
        rdict = {"Error": "Not logged in"}
        return JsonResponse(rdict, status=400)
    if compare_match(request.path,"/web_app/farm_access/"):
        return farm_access(request, user)
    if compare_match(request.path,"/web_app/farm_summary/"):
        return farm_summary(request, user)
    if compare_match(request.path,"/web_app/channel_summary/"):
        return channel_summary(request, user)
    if compare_match(request.path,"/web_app/robot_summary/"):
        return robot_summary(request, user)
    if compare_match(request.path,"/web_app/channel_update/light/"):
        return channel_update_light(request, user)
    if compare_match(request.path,"/web_app/channel_update/water/"):
        return channel_update_water(request, user)
    if compare_match(request.path,"/web_app/channel_update/water_temp/"):
        return channel_update_water_temp(request, user)
    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def verify_access_token(access_token):
    try:
        worker = workerAccount.objects.get(access_token=access_token).user
    except:
        return False, 0
    return True,worker

def verify_token(request, verification):
    if request.method == "GET":
        if verification == False:
            rdict = {"Success":"Success", "status":"invalid_token"}
            return JsonResponse(rdict, status=200)
        else:
            rdict = {"Success":"Success", "status":"valid_token"}
            return JsonResponse(rdict, status=200)
    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def farm_access(request, user):
    if request.method == "GET":
        cores = coreAccess.objects.filter(user=user)
        access_list = []
        i = 0
        while i < len(cores):
            access_list.append(cores[i].core.core_id)
            i += 1
        rdict = {"Success":"Success","core_ids":access_list}
        return JsonResponse(rdict, status=200)
    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def farm_summary(request, user):
    if request.method == "GET":
        try:
            core_id = int(request.GET.get('core_id'))
        except:
            rdict = {"Error": "core_id missing"}
            return JsonResponse(rdict, status=200)
        try:
            core = coreAccess.objects.get(user=user, core=core_id)
        except:
            rdict = {"Error":"No access to this farm"}
            return JsonResponse(rdict, status=200)
        sensor_data = []
        channels = channel.objects.filter(core__core_id=core_id)
        i =0
        while i < len(channels):
            values = {"water_status":channels[i].water.status_code, "light_status":channels[i].light.status_code, "overall":channels[i].status_code
                      }
            sensor_data.append({"channel_name":channels[i].name, "values":values})
            i += 1

        rdict = {"Success":"Success","sensor_data":sensor_data}
        return JsonResponse(rdict, status=200)

    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def channel_update_light(request, user):

    if request.method == "PUT":
        allDict = json.loads(request.body)
        try:
            core_id = allDict['core_id']
            channel_name = allDict['name']
            update_value = int(allDict['value'])
        except:
            rdict = {"Error": "core_id missing"}
            return JsonResponse(rdict, status=400)
        if update_value not in [-1, 0, 1]:
            rdict = {"Error":"Only values -1, 0, 1 allowed"}
            return JsonResponse(rdict, status=400)
        try:
            core = coreAccess.objects.get(user=user, core=core_id)
        except:
            rdict = {"Error":"No access to this farm"}
            return JsonResponse(rdict, status=400)
        sensor_data = []
        try:
            # Note
            single_channel = channel.objects.get(unique_id=str(core_id) + "-" + channel_name)
            single_channel.light.status_code = update_value
            if update_value == 1:
                single_channel.light.state = "ON"
                publish_information("light_status", "ON", 1)
            elif update_value == 0:
                single_channel.light.state = "OFF"
                publish_information("light_status", "OFF", 1)
            single_channel.light.save()
        except:
            rdict = {"Error":"No channel found"}
            return JsonResponse(rdict, status=400)

        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)

    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def channel_update_water(request, user):

    if request.method == "PUT":
        allDict = json.loads(request.body)
        try:
            core_id = allDict['core_id']
            channel_name = allDict['name']
            update_value = int(allDict['value'])
        except:
            rdict = {"Error": "core_id missing"}
            return JsonResponse(rdict, status=400)
        if update_value not in [-1, 0, 1]:
            rdict = {"Error":"Only values -1, 0, 1 allowed"}
            return JsonResponse(rdict, status=400)
        try:
            core = coreAccess.objects.get(user=user, core=core_id)
        except:
            rdict = {"Error":"No access to this farm"}
            return JsonResponse(rdict, status=400)
        sensor_data = []
        try:
            # Note
            single_channel = channel.objects.get(unique_id=str(core_id) + "-" + channel_name)
            single_channel.water.status_code = update_value
            if update_value == 1:
                single_channel.water.state = "ON"
                publish_information("water_status", "ON", 1)
            elif update_value == 0:
                single_channel.water.state = "OFF"
                publish_information("water_status", "OFF", 1)
            single_channel.water.save()
        except:
            rdict = {"Error":"No channel found"}
            return JsonResponse(rdict, status=400)

        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)

    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def channel_update_water_temp(request, user):

    if request.method == "PUT":
        allDict = json.loads(request.body)
        try:
            core_id = allDict['core_id']
            channel_name = allDict['name']
            update_value = int(allDict['value'])
        except:
            rdict = {"Error": "core_id missing"}
            return JsonResponse(rdict, status=400)
        try:
            core = coreAccess.objects.get(user=user, core=core_id)
        except:
            rdict = {"Error":"No access to this farm"}
            return JsonResponse(rdict, status=400)
        sensor_data = []
        try:
            # Note
            single_channel = channel.objects.get(unique_id=str(core_id) + "-" + channel_name)
            single_channel.water.ideal_temperature = update_value
            single_channel.water.save()
        except:
            rdict = {"Error":"No channel found"}
            return JsonResponse(rdict, status=400)

        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)

    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def channel_summary(request, user):

    if request.method == "GET":
        try:
            core_id = int(request.GET.get('core_id'))
            channel_name = str(request.GET.get('name'))
        except:
            rdict = {"Error": "core_id missing"}
            return JsonResponse(rdict, status=400)
        try:
            core = coreAccess.objects.get(user=user, core=core_id)
        except:
            rdict = {"Error":"No access to this farm"}
            return JsonResponse(rdict, status=400)
        sensor_data = []
        try:
            # Note
            single_channel = channel.objects.get(unique_id=str(core_id) + "-" + channel_name)
        except:
            rdict = {"Error":"No channel found"}
            return JsonResponse(rdict, status=400)

        water_values = {"ph":round(single_channel.water.ph, 1), "conduct":round(single_channel.water.conductivity),
                "temp":round(single_channel.water.temperature), "ideal_temp":round(single_channel.water.ideal_temperature),"state":single_channel.water.state}
        air_values = {"tvoc":round(single_channel.air.tvoc), "co2":single_channel.air.co2,
                      "temp":round(single_channel.air.temperature), "pressure":round(single_channel.air.pressure, 1),
                      "humidity":round(single_channel.air.humidity)
                      }
        light_values = {"spectro":round(single_channel.light.spectrum), "state":single_channel.light.state
                      }

        mass_values = {"mass":200, "height":2.3
                      }

        water_status = {"ph":True, "conduct":True,
                      "temp":False, "state":True}
        air_status = {"tvoc":True, "co2":True,
                      "temp":True, "pressure":True,
                      "humidity":True
                      }
        mass_status = {"spectro":True, "state":True
                      }

        light_status = {"mass":True, "height":True
                      }

        sensor_data = {"water_values":water_values, "air_values":air_values, "light_values":light_values,"mass_values":mass_values,
                            "light_status":light_status, "air_status":air_status, "water_status":water_status, "mass_status":mass_status,}

        rdict = {"Success":"Success","sensor_data":sensor_data}
        return JsonResponse(rdict, status=200)

    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def robot_summary(request, user):
    if request.method == "GET":
        try:
            core_id = int(request.GET.get('core_id'))
            cluster_id = str(1)
        except:
            rdict = {"Error": "core_id missing"}
            return JsonResponse(rdict, status=400)
        try:
            core = coreAccess.objects.get(user=user, core=core_id)
        except:
            rdict = {"Error":"No access to this farm"}
            return JsonResponse(rdict, status=400)
        try:
            # Note
            single_robot = robot.objects.get(joint_id=str(core_id) + "-" + cluster_id)
        except:
            rdict = {"Error":"No channel found"}
            return JsonResponse(rdict, status=400)
        stream_url = ""
        if single_robot.stream_link != "":
            stream_url = single_robot.stream_link
        rdict = {"Success":"Success","state":single_robot.status, "stream_url":stream_url}
        return JsonResponse(rdict, status=200)

    rdict = {"Error":"Unknown request type"}
    return JsonResponse(rdict, status=400)

def login(request):
    try:
        allDict = json.loads(request.body)
    except:
        rdict = {"Error": "Invalid body format"}
        return JsonResponse(rdict, status=400)
    try:
        username = str(allDict["username"])
    except:
        rdict = {"Error": "username missing"}
        return JsonResponse(rdict, status=400)
    try:
        password = allDict["password"]
    except:
        rdict = {"Error": "Password missing"}
        return JsonResponse(rdict, status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            worker = workerAccount.objects.get(user=user)
        except:
            rdict = {"Error": "Wrong account type"}
            return JsonResponse(rdict, status=200)
        access_token = ""
        while True:
            access_token = generate_key()
            exists, user = verify_access_token(access_token)
            if exists == False:
                worker.access_token = access_token
                worker.save()
                break
        rdict = {"Success": "Success", "access_token":access_token}

        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Invalid password"}
        return JsonResponse(rdict, status=400)


# core_id -> prevent alterations to other core_ids
# Worker web calls

