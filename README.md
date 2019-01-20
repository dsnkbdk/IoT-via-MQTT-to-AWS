# Raspberry Pi with AWS IoT platform
How to interact between AWS IoT platform and Raspberry-Pi

## Introduction
> Send a message/information from device(Raspberry Pi + sensor HAT) to the private cloud server through the MQTT protocol.

## Environment
* Device: Raspberry Pi + sensor HAT
* Programming: Python 3.0
* Cloud Server: AWS IoT
* Protocol: MQTT

## Import libraries
* Paho : MQTT Client library for python > `pip install paho-mqtt`
* ssl : security
* time : time.sleep()

## Code Description
* aws_mqtt_pub.py: This is for publish. Need to set own `host-url` and `certification files` downloaded from AWS IoT in the same root.
* aws_mqtt_sub.py: This is for subscribe. Open the terminal in Raspberry Pi, then run it. Open the another terminal and then run the pub.py files. You can get the message on the subscribe terminal.

## Created by Unha Back, Giang Hoang Le, Wennan Shi

## References
* AWS Connecting Raspberry Pi: https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdk-setup.html
