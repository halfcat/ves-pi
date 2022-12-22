#!/usr/bin/python3
'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json
import math
import random
import logging
import threading

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print(f"Received a new message from topic {message.topic}: ")
    print(message.payload)
    print("--------------\n\n")

class PubSub:
    logger = None
    port = 8883 # MQTT default port
    myAWSIoTMQTTClient = None
    topic = None

    host = 'a16lgnsxwcv0l8-ats.iot.us-east-1.amazonaws.com'
    rootCAPath = '/Users/cwhowell/certs/AmazonRootCA1.pem'
    certificatePath = '/Users/cwhowell/certs/63GL-cert.pem.crt'
    privateKeyPath = '/Users/cwhowell/certs//63GL-private.pem.key'
    clientId = '63GL'
    is_online = False

    def __init__(self,topic=None):
        self.topic = topic
        # Read in command-line parameters
        parser = argparse.ArgumentParser()
        #parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
        #parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
        parser.add_argument("-e", "--endpoint", action="store", dest="host", help="Your AWS IoT custom endpoint")
        parser.add_argument("-r", "--rootCA", action="store", dest="rootCAPath", help="Root CA file path")
        parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
        parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
        parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
        parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                                help="Use MQTT over WebSocket")
        parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="63GL",
                                help="Targeted client id")
        parser.add_argument("-t", "--topic", action="store", dest="topic", default="ves-pi/motor", help="Targeted topic")
        parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                                help="Operation modes: %s"%str(AllowedActions))
        parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                                help="Message to publish")

        self.args = parser.parse_args()
        if self.args.host:
            self.host = self.args.host
        if self.args.rootCAPath:
            self.rootCAPath = self.args.rootCAPath
        if self.args.certificatePath:
            self.certificatePath = self.args.certificatePath
        if self.args.privateKeyPath:
            self.privateKeyPath = self.args.privateKeyPath
        if self.args.port:
            self.port = self.args.port
        self.useWebsocket = self.args.useWebsocket
        if self.args.clientId:
            self.clientId = self.args.clientId
        if topic:
            self.topic = self.args.topic

        #if args.mode not in AllowedActions:
            #parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
            #exit(2)

        #if args.useWebsocket and args.certificatePath and args.privateKeyPath:
            #parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
            #exit(2)

        #if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
            #parser.error("Missing credentials for authentication.")
            #exit(2)

        # Port defaults
        if self.args.useWebsocket and not self.args.port:  # When no port override for WebSocket, default to 443
            self.port = 443
        if not self.args.useWebsocket and not self.args.port:  # When no port override for non-WebSocket, default to 8883
            self.port = 8883

        self.init_client()

    # set up logging, or force re-initialization if force_reinit is True
    def configure_logger(self, force_reinit=False):
        if self.logger == None or force_reinit == True:
            # Configure logging
            self.logger = logging.getLogger("AWSIoTPythonSDK.core")
            self.logger.setLevel(logging.INFO)
            streamHandler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            streamHandler.setFormatter(formatter)
            self.logger.addHandler(streamHandler)


    def init_client(self, force_reinit=False):
        # Init AWSIoTMQTTClient
        if force_reinit == True:
            self.myAWSIoTMQTTClient = None
        if self.myAWSIoTMQTTClient != None:
            return

        if self.useWebsocket:
            print("Using WebSocket")
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId, useWebsocket=True)
            self.myAWSIoTMQTTClient.configureEndpoint(self.host, self.port)
            self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath)
        else:
            print("Using MQTT")
            print("clientId:", self.clientId)
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)
            #print(f"Endpoint: {self.host}:{self.port}")
            self.myAWSIoTMQTTClient.configureEndpoint(self.host, self.port)
            print("Keys:  %s  %s  %s", self.rootCAPath, self.privateKeyPath, self.certificatePath)
            self.myAWSIoTMQTTClient.configureCredentials(
                self.rootCAPath, self.privateKeyPath, self.certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 seo
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        self.myAWSIoTMQTTClient.onOnline = self.online_event_callback
        self.myAWSIoTMQTTClient.onOffline = self.offline_event_callback

    def online_event_callback(self):
        self.is_online = True

    def offline_event_callback(self):
        print("went offline :(")
        self.is_online = False
        logging.warning("went offline :(")

    def connect(self):
        try:
            self.myAWSIoTMQTTClient.connect()
            self.is_online = True
        except ConnectTimeoutException as cte:
            self.is_online = False
            logging.error("*** Failed to connect!  Connection attempt timed out!")
            logging.error(cte)

    def subscribe(self, topic):
        #if args.mode == 'both' or args.mode == 'subscribe':
        self.myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
        #time.sleep(2)

    #publish a message consisting of a dict which will be converted into a json document for sending
    def publish(self, message={}):
        messageJson = json.dumps(message)
        if self.myAWSIoTMQTTClient:
            print( "Message JSON:", messageJson)
            try:
                self.myAWSIoTMQTTClient.publish(self.topic, messageJson, 1)
            except Exception as pte:
                print("Unable to publish! Attempting reconnection...")
                self.myAWSIoTMQTTClient.connect()
        else:
            print("No connection...reconnecting...")
            logging.info("No connection...reconnecting...")
            self.myAWSIoTMQTTClient.connect()
        #       self.myAWSIoTMQTTClient.subscribe(self.topic)

if __name__ == "__main__":
    ps = PubSub(topic='ves-pi/63GL')
    ps.configure_logger()
    print("Connecting...")
    ps.connect()
    print("Connected.")
    if False:
        print("Subscribing...'ves-pi/63GL/responses'")
        ps.subscribe('ves-pi/63GL/responses')
        print("Subscribed.")

    # create the Gear
    logging.info("Initializing gear position sensor")
    #    from gear import Gear
    #gear = Gear()
    class Gear:
        gears = ['1', '0', '2', '3', '4']
        def gear(self):
            return random.randint(0,4)

    gear = Gear()

    # Create the Throttle
    logging.info("Initializing throttle position sensor")
    #from throttle import Throttle
    class Throttle:
        def percent(self):
            return random.randint(0,100)
    throttle = Throttle()

    # Create the CHT
    logging.info("Initializing Cylinder Head Temp (CHT)")
    class Cht:
        def temperature(self):
            return random.randint(70,400)
    cht = Cht()

    logging.info("Initializing Exhaust Gas Temp (EGT)")
    class Egt:
        def temperature(self):
            return random.randint(900,1600)

    egt = Egt()
    # Create the speed & position (GPS)
    logging.info("Initializing GPS")

    class Gps:
        def speed(self):
            return random.randint(0,92)
        def latitude(self):
            return 44.126
        def longitude(self):
            return 45.127
        def altitude(self):
            return 300
    gps = Gps()

    # Create the Tach
    logging.info("Initializing Tachometer")
    class Tach:
        def rpms(self):
            return random.randint(1200,10000)

    tach = Tach()

    # Create the Accelerometer
    logging.info("Initializing Accelerometer")

    class Accelerometer:
        def x(self):
            return 0
        def y(self):
            return 0
        def z(self):
            return 0
    accelerometer = Accelerometer()

    # Create the clutch
    # TODO:  Install a clutch sensor
    class Clutch:
        in_gear = True
    clutch = Clutch()


    class Motor:
        _rpms = 1200
        gear = 1 # neutral
        wheel_diameter = 1316 # mm
        _speed = 0

        def __init__(self):
            self._rpms = 1200
            self.gear = 1
            self._speed = 0
        gear_ratios = [
            14.74, # 1st
            9.80,
            7.06,
            5.31   # 4th
        ]

        def clutch_slip(self):
            if self._speed == 0:
                return 0

#            if self._speed / self.gear_ratios[self._gear-1]
            gear_speed = int(((self._rpms * self.wheel_diameter) / (self.gear_ratios[self.gear-1] * 16667)) * 0.621371) 
            slip = gear_speed - self._speed
            return slip
        def speed(self):
            # this will show zero if in neutral, regardless of "actual" speed
            if self.gear == 0:
                self._speed *= 0.9
                return self._speed
            self._speed = int(((self._rpms * self.wheel_diameter) / (self.gear_ratios[self.gear-1] * 16667)) * 0.621371)
            # Simulate clutch slip from 5-8k RPM's
            if self._rpms > 5000 and self._rpms < 8000:
                self._speed *= 0.8
            return max(0, self._speed)

        def rpms(self):
            self._rpms += 100
            if self._rpms > 10000:
                self._rpms = 1200
                if self.gear == 0: # neutral goes into gear
                    self.gear = 1
                elif self.gear < 4: # upshift
                    self.gear += 1
                else:
                    self.gear = 0 # back to neutral
            return self._rpms

        def cht(self):
            return (self._rpms/10000) * 350

        def egt(self):
            return (self._rpms/10000) * 1800

        def throttle(self):
            return int(self._rpms/100)

        #def gear(self):
        #    return self.gear

    m = Motor()

    print(f'Publishing to topic {ps.topic}')
    loopCount = 0
    #while loopCount < 1000:
    while True:
        message = { 'device': '63GL',
                'payload': {
                        'timestamp': str(math.trunc(time.time()*1000)),
                        'gear': m.gear,
                        'cht': m.cht(),
                        'egt': m.egt(),
                        'rpms': m.rpms(),
                        'clutch_slip': m.clutch_slip(),
                        'throttle': m.throttle(),
                        'clutch': clutch.in_gear,
                        'position': {
                                'lat': gps.latitude(),
                                'long': gps.longitude(),
                                'altitude': gps.altitude()
                        },
                        'speed': m.speed(),
                        'acceleration': {
                                'x': accelerometer.x(),
                                'y': accelerometer.y(),
                                'z': accelerometer.z()
                        }
                }
        }
        ps.publish(message)
        print( "Published topic "+ps.topic + " " + str(message) )
        loopCount += 1
        #time.sleep(.2)
        time.sleep(.5)
