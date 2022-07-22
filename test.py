from pyPS4Controller.controller import Controller
from paho.mqtt import client as mqtt_client
import random
import logging

broker = 'test.mosquitto.org'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''

logger = logging.Logger('basic_logger', level=logging.DEBUG)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        publish(client, "Custom x press message")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, msg="<empty message>"):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

client = connect_mqtt()
def run():
    client.loop_start()
    publish(client)
    controller.listen()


if __name__ == '__main__':
    run()