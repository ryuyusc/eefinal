import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
from datetime import datetime
import time
from prettytable import PrettyTable

#encryption key
key = 'GynZhrE8XGJwDeoSSKu8MAnwawL_NZtU8tXspajt56U='
cipher = Fernet(key.encode('utf-8'))

# creates broker address and topic
broker = "test.mosquitto.org"
topic = "ryuyb/final"

# for creating the table
table = PrettyTable()
table.field_names = ["Time", "Actual Temperature", "Actual Humidity", "Open Weather Temperature", "Open Weather Humidity"]

# For adding entry to table
def add_entry(dateAndtime, point1, point2, point3, point4):
    table.add_row([dateAndtime, point1, point2, point3, point4])

#callback for when connected
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))
    client.subscribe(topic)


#callback for when message received
def on_message(client, userdata, msg):
    #decrypts data
    decrypted = cipher.decrypt(msg.payload)

    #converts bytes to tuple
    message = eval(decrypted.decode('utf-8'))

    print(message)

    time = datetime.now()
    realTemp, realHum, OWTemp, OWHum = message

    #adds entry to table
    add_entry(time, realTemp, realHum, OWTemp, OWHum)

    #shows table with all new values
    print(table)


if __name__ == '__main__':

    # creates client and callback
    client = mqtt.Client()
    client.on_message = on_message

    #connect to broker
    client.connect(broker, 1883, 60)

    client.loop_start()

    while True:
        time.sleep(1)

