import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
from datetime import datetime
import time

#encryption key
key = b'VgEBRr6rb8VCTYjGBa4vZ1AOT-ubFmPp4NlSszLFoT'
cipher = Fernet(key)

# creates broker address and topic
broker = "test.mosquitto.org"
topic = "final"

#callback for when connected
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe(topic)


#callback for when message received
def on_message(client, userdata, msg):
    #decrypts data
    decrypted = cipher.decrypt(msg.payload)

    #converts bytes to tuple
    message = eval(decrypted.decode())

    print(message)
    print(datetime.now())
    

if __name__ == '__main__':
    # creates client and callback
    client = mqtt.Client()
    client.on_message = on_message

    #connect to broker
    client.connect(broker, 1883, 60)

    client.loop_start()

    while True:
        time.sleep(1)

