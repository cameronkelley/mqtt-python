import time
import shlex
import sys
import subprocess
import paho.mqtt.client as mqtt

broker="192.168.0.109"
terminate=""

camera_start_command = ['/bin/bash', 'start_helper.sh']
camera_stop_command = ['/bin/bash', 'stop_helper.sh']

sub_topics = {
    "start" : "pi-white/camera/#",
}
pub_topics = {
    "status" : "pi-white/camera/status"
}

def on_message(client, userdata, message):
    time.sleep(1)
    # message_data=str(message.payload.decode("utf-8"))
    # print(f"Data: {message_data}")
    # print(f"Topic: {message.topic}")
    # print(f"QOS: {message.qos}")
    # print(f"Retain: {message.retain}")

    if message.topic == sub_topics["start"]:
        print("Starting camera stream")
        subprocess.run(camera_start_command)

    if message.topic == sub_topics["stop"]:
        print("Stopping camera stream")
        subprocess.run(camera_stop_command)

    if message.topic == sub_topics["terminate"]:
        print("Diconnect topic true")
        client.disconnect()
        
# def on_publish(client, userdata, mid):

def on_disconnect(client, userdata, rc):
    global terminate
    time.sleep(1)
    if rc != 0:
        print("Connection terminated unexpectedly")
    else:
        print("Disconnected cleanly")
    time.sleep(1)
    client.loop_stop()
    time.sleep(2)
    terminate = "True"

def start_camera():
    print("Starting camera stream")
    subprocess.run(camera_start_command)
    client.publish(pub_topics["status"], "started")

def stop_camera():
    print("Stopping camera stream")
    subprocess.run(camera_stop_command)
    client.publish(pub_topics["status"], "stopped")

client= mqtt.Client()

######Bind function to callback
client.on_message=on_message
client.on_disconnect=on_disconnect
#####

print("Connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages

for sub, topic in sub_topics.items():
    print(f"Subscribing to {topic}")
    client.subscribe(topic)

client.publish(pub_topics["status"], "Script started")

while terminate != "True":
    time.sleep(3)

client.publish(pub_topics["status"], "Script terminated")
sys.exit()
