import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
import grovepi
import geocoder
import requests
import time

# grovepi button port
BT_PORT = 3

# grovepi temperature and humidity port
TEMP_PORT = 2

# this is for encryption purposes
key = 'GynZhrE8XGJwDeoSSKu8MAnwawL_NZtU8tXspajt56U='

cipher = Fernet(key.encode('utf-8'))

# creates broker address and topic
topic = "ryuyb/final"

# API website and key
API_SITE = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = '4cc919c4981eb59f9f4ffd541c6a1626'


# connection callback
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code" + str(rc))

# callback when message published
def on_publish(client, userdata, mid):
    print("sent")

# grabbing data from the OpenWeather API
#returns tuple of [temperature, humidity]
def get_data():
    # grabs location information using geocoder
    location = geocoder.ip('me')
    lat = location.latlng[0]
    long = location.latlng[1]

    #creates parameters
    params = {
        'appid': API_KEY,
        'lat': lat,
        'lon': long,
        'units': 'imperial',
    }

    response = requests.get(API_SITE, params)

    #extracts temperature and humidity if successful
    if response.status_code == 200:
        data = response.json()
        return (data.get("main").get("temp"), data.get("main").get("humidity"))
    
    #error
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0





if __name__ == '__main__':

    #sets the pins
    grovepi.pinMode(BT_PORT, "INPUT")
    grovepi.pinMode(TEMP_PORT, "INPUT")

    # creates MQTT client
    client = mqtt.Client()

    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    client.on_publish = on_publish

    # starts loop of checking whether button is pressed
    while True:
        if (grovepi.digitalRead(BT_PORT) == 1):
            #grabs data from the temperature and humidity sensor
            [temperature, humidity] = grovepi.dht(TEMP_PORT, 0)

            # grabs data from the openweather API
            api_temp, api_hum = get_data()

            # creates tuple to send that has all the data
            data_toSend = (temperature , humidity, api_temp, api_hum)

            print(data_toSend)

            #convert data to bytes
            data_bytes = str(data_toSend).encode()

            #encryption
            encrypted = cipher.encrypt(data_bytes)

            client.publish(topic, encrypted)
            time.sleep(1)