import paho.mqtt.client as mqtt #import the client1
from os import urandom

def compare_match(path, ideal_path):
    if path[:len(ideal_path)] == ideal_path or path == ideal_path[:-1]:
        return True
    else:
        return False

def generate_key():
    length = 16
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(chars[ord(c) % len(chars)] for c in urandom(length))

#broker_address="192.168.0.38"
broker_address="iot.eclipse.org" #use external broker
channel_history = {}
def publish_information(channel, data, id):
    client = mqtt.Client("P1") #create new instance
    client.connect(broker_address, port=1883) #connect to broker
    client.publish("green_earth/"+channel,str(data)+" " + str(id))