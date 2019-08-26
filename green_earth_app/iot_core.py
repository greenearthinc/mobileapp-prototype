import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from sensor_models import waterCluster, airCluster, lightCluster, robot, iotCore
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from support_files import compare_match
# types = ["air_tvoc", "air_co2", "air_temp", "air_pressure", "air_humidity", "water_temp", "water_ph", "water_conduct","light_spectro", "light_status", "robot_status"]

# Check login
# Retrieve all data from farm

@csrf_exempt
def iot_core_router(request):
    if compare_match(request.path,"/iot_core/login/"):
        return login(request)
    if request.user.is_authenticated == False:
        rdict = {"Error": "Not logged in"}
        return JsonResponse(rdict, status=400)
    # check core_id, cluster_id here
    core_id = int(request.user.username.replace("core_id_",""))
    try:
        core = iotCore.objects.get(core_id=core_id)
    except:
        rdict = {"Error": "Server error"}
        return JsonResponse(rdict, status=400)
    rdict = check_iot_core(request)
    if "Error" in rdict:
        return JsonResponse(rdict, status=400)
    # see if logged in; otherwise error
    if compare_match(request.path,"/iot_core/air/"):
        return air_router(request, core)
    if compare_match(request.path,"/iot_core/water/"):
        return water_router(request, core)
    if compare_match(request.path,"/iot_core/light/"):
        return light_router(request, core)
    if compare_match(request.path,"/iot_core/robot/"):
        return robot_router(request, core)
    rdict = {"Error": "Unknown request"}
    return JsonResponse(rdict, status=400)

def air_router(request, core):
    if compare_match(request.path,"/iot_core/air/temp/"):
        return air_temp_router(request, core)
    if compare_match(request.path,"/iot_core/air/co2/"):
        return air_co2_router(request, core)
    if compare_match(request.path,"/iot_core/air/tvoc/"):
        return air_tvoc_router(request, core)
    if compare_match(request.path,"/iot_core/air/pressure/"):
        return air_pressure_router(request, core)
    if compare_match(request.path,"/iot_core/air/humidity/"):
        return air_humidity_router(request, core)
    rdict = {"Error": "Unknown request"}
    return JsonResponse(rdict, status=400)

def water_router(request, core):
    if compare_match(request.path,"/iot_core/water/temp/"):
        return water_temp_router(request, core)
    if compare_match(request.path,"/iot_core/water/ph/"):
        return water_ph_router(request, core)
    if compare_match(request.path,"/iot_core/water/conduct/"):
        return water_conduct_router(request, core)
    rdict = {"Error": "Unknown request"}
    return JsonResponse(rdict, status=400)

def light_router(request, core):
    if compare_match(request.path,"/iot_core/light/spectro/"):
        return light_spectro_router(request, core)
    if compare_match(request.path,"/iot_core/light/status/"):
        return light_status_router(request, core)
    rdict = {"Error": "Unknown request"}
    return JsonResponse(rdict, status=400)

def robot_router(request, core):
    if compare_match(request.path,"/iot_core/robot/status/"):
        return robot_status_router(request, core)
    if compare_match(request.path,"/iot_core/robot/address/"):
        return robot_address_router(request, core)
    rdict = {"Error": "Unknown request"}
    return JsonResponse(rdict, status=400)

def login(request):
    try:
        allDict = json.loads(request.body)
    except:
        rdict = {"Error": "Invalid body format"}
        return JsonResponse(rdict, status=400)
    try:
        username = "core_id_" + str(allDict["core_id"])
    except:
        rdict = {"Error": "core_id missing"}
        return JsonResponse(rdict, status=400)
    try:
        access_token = allDict["access_token"]
    except:
        rdict = {"Error": "Access token missing"}
        return JsonResponse(rdict, status=400)
    user = authenticate(username=username, password=access_token)
    if user is not None:
        rdict = {"Success": "Success"}
        auth_login(request, user)
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Invalid access token"}
        return JsonResponse(rdict, status=400)


def check_iot_core(request):
    try:
        allDict = json.loads(request.body)
    except:
        return {"Error":"Invalid body format"}
    try:
        cluster_id = int(allDict["cluster_id"])
    except:
        return {"Error":"Missing cluster_id"}
    return {}

def return_or_create_air_cluster(allDict, core):
    core_id = core.core_id
    cluster_id = int(allDict['cluster_id'])
    joint_id = str(core_id) + "-" + str(cluster_id)
    print(joint_id)
    try:
        cluster = airCluster.objects.get(joint_id=joint_id)
    except:
        cluster = airCluster()
        cluster.joint_id = joint_id
        cluster.core = core
        cluster.cluster_id = cluster_id
        cluster.save()
        print("saved")
    return cluster

def return_or_create_water_cluster(allDict, core):
    core_id = core.core_id
    cluster_id = int(allDict['cluster_id'])
    joint_id = str(core_id) + "-" + str(cluster_id)
    print(joint_id)
    try:
        cluster = waterCluster.objects.get(joint_id=joint_id)
    except:
        cluster = waterCluster()
        cluster.joint_id = joint_id
        cluster.core = core
        cluster.cluster_id = cluster_id
        cluster.save()
        print("saved")
    return cluster

def return_or_create_light_cluster(allDict, core):
    core_id = core.core_id
    cluster_id = int(allDict['cluster_id'])
    joint_id = str(core_id) + "-" + str(cluster_id)
    print(joint_id)
    try:
        cluster = lightCluster.objects.get(joint_id=joint_id)
    except:
        cluster = lightCluster()
        cluster.joint_id = joint_id
        cluster.core = core
        cluster.cluster_id = cluster_id
        cluster.save()
        print("saved")
    return cluster

def return_or_create_robot(allDict, core):
    core_id = core.core_id
    cluster_id = int(allDict['cluster_id'])
    joint_id = str(core_id) + "-" + str(cluster_id)
    try:
        cluster = robot.objects.get(joint_id=joint_id)
    except:
        cluster = robot()
        cluster.joint_id = joint_id
        cluster.core = core
        cluster.cluster_id = cluster_id
        cluster.save()
        print("saved")
    return cluster


def air_temp_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_air_cluster(allDict, core)
        try:
            cluster.temperature = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def air_co2_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_air_cluster(allDict, core)
        try:
            cluster.co2 = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def air_tvoc_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_air_cluster(allDict, core)
        try:
            cluster.tvoc = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def air_pressure_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_air_cluster(allDict, core)
        try:
            cluster.pressure = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def air_humidity_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_air_cluster(allDict, core)
        try:
            cluster.humidity = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def water_temp_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_water_cluster(allDict, core)
        try:
            cluster.temperature = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def water_ph_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_water_cluster(allDict, core)
        try:
            cluster.ph = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def water_conduct_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_water_cluster(allDict, core)
        try:
            cluster.conductivity = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def light_spectro_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_light_cluster(allDict, core)
        try:
            cluster.spectrum = float(allDict['value'])
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def light_status_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        cluster = return_or_create_light_cluster(allDict, core)
        try:
            cluster.state = str(allDict['value'])
            if cluster.status == "ON":
                cluster.status_code = 1
            elif cluster.status == "OFF":
                cluster.status_code = 0
            cluster.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def robot_status_router(request, core):
    print(request.path)
    if request.method == "PUT":
        allDict = json.loads(request.body)
        robot = return_or_create_robot(allDict, core)
        try:
            robot.status = str(allDict['value'])
            robot.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)

def robot_address_router(request, core):
    if request.method == "PUT":
        allDict = json.loads(request.body)
        robot = return_or_create_robot(allDict, core)
        try:
            robot.stream_link = str(allDict['ip_address'])
            robot.save()
        except:
            rdict = {"Error": "Missing parameter"}
            return JsonResponse(rdict, status=400)
        rdict = {"Success":"Success"}
        return JsonResponse(rdict, status=200)
    else:
        rdict = {"Error": "Unknown request"}
        return JsonResponse(rdict, status=400)