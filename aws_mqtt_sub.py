# Import packages
import paho.mqtt.client as mqtt
import ssl

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 30
MQTT_TOPIC1 = "rasphat/sensors"
MQTT_TOPIC2 = "rasphat/joystick"
MQTT_TOPIC3 = "rasphat/magnetometer"

# Cloud Configuration (Host, Certification file, Private Key)
MQTT_HOST = "aoscy1wztqxzf.iot.ap-southeast-1.amazonaws.com"
CA_ROOT_CERT_FILE = "./root-CA.crt"
THING_CERT_FILE = "./MyCertificate.pem.crt"
THING_PRIVATE_KEY = "./MyPrivate.pem.key"

# Define on connect event function
# Subscribe to our Topic in this function
def on_connect(mosq, obj, flags, rc):
    mqttc.subscribe(MQTT_TOPIC1, 0)
    mqttc.subscribe(MQTT_TOPIC2, 0)
    mqttc.subscribe(MQTT_TOPIC3, 0)

# Define on_message event function. 
# This function will be invoked every time,
# a new message arrives for the subscribed topic 
def on_message(mosq, obj, msg):
    print("=========================================================================")
	print("Topic: " + str(msg.topic))
	print("QoS: " + str(msg.qos))
	print("Payload: " + str(msg.payload))
    print("=========================================================================")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed Topics : " + 
	MQTT_TOPIC1 + "," + MQTT_TOPIC2 + "," + MQTT_TOPIC3 + "," + " with QoS: " + str(granted_qos))
    print("=========================================================================")

# Initiate MQTT Client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()
