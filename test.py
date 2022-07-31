from pyPS4Controller.controller import Controller
from paho.mqtt import client as mqtt_client
import random
import logging

broker = 'test.mosquitto.org'
port = 1883
topic = "python/mqtt/ds4msg"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''

logging.basicConfig(
    format='[ds4MQTT][%(asctime)s]\t[%(levelname)s]\t%(message)s',
    level=logging.DEBUG
)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        msg = "Custom x press message"
        logging.debug(msg)
        publish(client, msg)


def on_message(client, userdata, message):
    logging.info("Message received: "  + str(message.payload))

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
    client.on_message = on_message
    client.connect(broker, port)
    return client

def publish(client, msg="<empty message>"):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        logging.info(f"Sent `{msg}` to topic `{topic}`")
    else:
        logging.warn(f"Failed to send message to topic {topic}")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

client = connect_mqtt()
def run():
    client.loop_start()
    client.subscribe(topic)
    publish(client)
    controller.listen()


if __name__ == '__main__':
    run()