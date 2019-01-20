# Import packages
import paho.mqtt.client as mqtt
import ssl
import time
from sense_hat import SenseHat

sense = SenseHat()

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 30

# Cloud Configuration (Host, Certification file, Private Key)
MQTT_HOST = "aoscy1wztqxzf.iot.ap-southeast-1.amazonaws.com"
CA_ROOT_CERT_FILE = "./root-CA.crt"
THING_CERT_FILE = "./MyCertificate.pem.crt"
THING_PRIVATE_KEY = "./MyPrivate.pem.key"

# MQTT Toppic setting
MQTT_TOPIC1 = "hat/sensors"
MQTT_TOPIC2 = "hat/joystick"
MQTT_TOPIC3 = "hat/magnetometer"

# Sensors Message Form
MQTT_MSG1 = "Temperature: {0:.0f}C, Humidity: {1:0.2f}%, Pressure: {2:.0f}mbar".format(sense.get_temperature(),sense.get_humidity(),sense.get_pressure())

# Define callback function for publishing
def on_publish(client, userdata, mid):
	print("A message published successfully!")
	
# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)		
mqttc.loop_start()

# Direction disply map
p = (204,0,204) # pink
g = (0, 102, 102) # Green
w = (200, 200, 200) # White
y = (204, 204, 0) # Yellow
e = (0, 0, 0) # Empty

# Display direction
left = [
    e, e, e, p, p, e, e, e,
    e, e, p, p, e, e, e, e,
    e, p, p, e, e, e, e, e,
    p, p, p, p, p, p, p, p,
    p, p, p, p, p, p, p, p,
    e, p, p, e, e, e, e, e,
    e, e, p, p, e, e, e, e,
    e, e, e, p, p, e, e, e,
]

right = [
    e, e, e, g, g, e, e, e,
    e, e, e, e, g, g, e, e,
    e, e, e, e, e, g, g, e,
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    e, e, e, e, e, g, g, e,
    e, e, e, e, g, g, e, e,
    e, e, e, g, g, e, e, e,
]

up = [
    e, e, e, w, w, e, e, e,
    e, e, w, w, w, w, e, e,
    e, w, w, w, w, w, w, e,
    w, w, e, w, w, e, w, w,
    w, e, e, w, w, e, e, w,
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e,
    e, e, e, w, w, e, e, e,
]

down = [
    e, e, e, y, y, e, e, e,
    e, e, e, y, y, e, e, e,
    e, e, e, y, y, e, e, e,
    y, e, e, y, y, e, e, y,
    y, y, e, y, y, e, y, y,
    e, y, y, y, y, y, y, e,
    e, e, y, y, y, y, e, e,
    e, e, e, y, y, e, e, e,
]

# Send magnetometer and sensors information every second and 50 times
count = 0

while (count < 50):
    # Publish Sensor info
    mqttc.publish(MQTT_TOPIC1,MQTT_MSG1,qos=1)
    # Magnetometer actions
    north = sense.get_compass() # Get compass data
    MQTT_MSG3 = "North: {0:.0f} Degree".format(north)
    mqttc.publish(MQTT_TOPIC3,MQTT_MSG3,qos=1)
    # Joystick action - show the direction on the display
    for event in sense.stick.get_events():
        MQTT_MSG2 = "The joystick was moving {}".format(event.direction)
        if event.direction == 'left':
            sense.set_pixels(left)
            time.sleep(1)
            sense.clear()
        elif event.direction == 'right':
            sense.set_pixels(right)
            time.sleep(1)
            sense.clear()
        elif event.direction == 'up':
            sense.set_pixels(up)
            time.sleep(1)
            sense.clear()
        elif event.direction == 'down':
            sense.set_pixels(down)
            time.sleep(1)
            sense.clear()
        mqttc.publish(MQTT_TOPIC2,MQTT_MSG2,qos=1)
    time.sleep(1)
    count += 1
    
# Disconnect from MQTT_Broker
# mqttc.disconnect()
