import requests
import json

core_id = 1
user = 'core_id_' + str(core_id)
base_URL = "http://35.203.115.88:8000/"
session = None
access_token = ""

def login(core_id_l, access_token_l):
    global access_token
    access_token = access_token_l
    global core_id
    core_id = core_id_l
    data = json.dumps({'core_id': core_id, 'access_token': access_token})
    global session
    session = requests.Session()
    r = session.put(base_URL+"iot_core/login/", data=data)
    r = json.loads(r.text)
    if "Error" in r:
        print(r)

def error_handle_update(r):
    try:
        r = json.loads(r.text)
    except:
        print({"Error":"No data received"})
    if "Error" in r:
        print(r)
        if r["Error"] == "Not logged in":
            login(core_id, access_token)


def update_air_temp(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/air/temp/", data=data)
    error_handle_update(r)

def update_air_co2(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/air/co2/", data=data)
    error_handle_update(r)

def update_air_tvoc(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/air/tvoc/", data=data)
    error_handle_update(r)

def update_air_pressure(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/air/pressure/", data=data)
    error_handle_update(r)

def update_air_humidity(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/air/humidity/", data=data)
    error_handle_update(r)

def update_water_temp(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/water/temp/", data=data)
    error_handle_update(r)

def update_water_ph(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/water/ph/", data=data)
    error_handle_update(r)

def update_water_conduct(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/water/conduct/", data=data)
    error_handle_update(r)

def update_light_spectro(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/light/spectro/", data=data)
    error_handle_update(r)

def update_light_status(cluster_id, value):
    data = json.dumps({'cluster_id': cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/light/status/", data=data)
    error_handle_update(r)

def update_robot_status(cluster_id ,value):
    data = json.dumps({'cluster_id':cluster_id, 'value': value})
    r = session.put(base_URL+"iot_core/robot/status/", data=data)
    error_handle_update(r)

key = "BY2UFPW58CQWSY3X"
login(1, key)
update_air_temp(10, 22.4)
update_air_co2(10, 100)
update_air_tvoc(10, 144)
update_air_pressure(9, 120)
update_air_humidity(9, 99.8)
update_water_temp(11, 22)
update_water_ph(11, 7)
update_water_conduct(12, 0.2)
update_light_spectro(16, 620)
update_light_status(16, "OFF")
update_robot_status(18, "Trimming matured cannabis")

# Then add to subscriptions

