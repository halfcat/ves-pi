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
import board
import logging
import time
import argparse
import json
import math

from temp_sensor import TempSensor

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

class PubSub:
	logger = None
	port = 8883 # MQTT default port
	myAWSIoTMQTTClient = None
	topic = None
	host = 'a16lgnsxwcv0l8-ats.iot.us-east-1.amazonaws.com'
	rootCAPath = '/home/pi/63GL/root-CA.crt'
	certificatePath = '/home/pi/63GL/63GL.cert.pem'
	privateKeyPath = '/home/pi/63GL/63GL.private.key'
	clientId = '63GL'

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
			self.logger.setLevel(logging.DEBUG)
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
			logging.info("Using WebSocket")
			self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId, useWebsocket=True)
			self.myAWSIoTMQTTClient.configureEndpoint(self.host, self.port)
			self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath)
		else:
			print("Using MQTT")
			logging.info("Using MQTT")
			print("clientId:", self.clientId)
			self.myAWSIoTMQTTClient = AWSIoTMQTTClient(self.clientId)
			#print(f"Endpoint: {self.host}:{self.port}")
			self.myAWSIoTMQTTClient.configureEndpoint(self.host, self.port)
			print("Keys:  %s  %s  %s", self.rootCAPath, self.privateKeyPath, self.certificatePath)
			self.myAWSIoTMQTTClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

		# AWSIoTMQTTClient connection configuration
		self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
		self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 seo
		self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

	def connect(self):
		self.myAWSIoTMQTTClient.connect()

	def subscribe(self, topic):
		#if args.mode == 'both' or args.mode == 'subscribe':
		self.myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
		time.sleep(2)

	#publish a message consisting of a dict which will be converted into a json document for sending
	def publish(self, message={}):
		messageJson = json.dumps(message)
		if self.myAWSIoTMQTTClient:
			print( "Message JSON:", messageJson)
			self.myAWSIoTMQTTClient.publish(self.topic, messageJson, 1)
		else:
			print("No connection...reconnecting...")
			self.myAWSIoTMQTTClient.connect()
			self.myAWSIoTMQTTClient.subscribe(self.topic)
		
	'''
	def truncate(self, number, decimals=0):
		"""
		Returns a value truncated to a specific number of decimal places.
		"""
		if not isinstance(decimals, int):
			raise TypeError("decimal places must be an integer.")
		elif decimals < 0:
			raise ValueError("decimal places has to be 0 or more.")
		elif decimals == 0:
			return math.trunc(number)

		factor = 10.0 ** decimals
		return math.trunc(number * factor) / factor
	'''

if __name__ == "__main__":
	ps = PubSub(topic='ves-pi/63GL')
	print("Connecting...")
	ps.connect()
	print("Connected.")
	if False:
		print("Subscribing...'ves-pi/63GL/responses'")
		ps.subscribe('ves-pi/63GL/responses')
		print("Subscribed.")

	# create the Gear 
	logging.info("Initializing gear position sensor")
	from gear import Gear
	gear = Gear()

	# Create the Throttle 
	logging.info("Initializing throttle position sensor")
	from throttle import Throttle
	throttle = Throttle()

	# Create the CHT 
	logging.info("Initializing Cylinder Head Temp (CHT)")
	from temp_sensor import TempSensor
	cht = TempSensor(board.D5)

	# Create the CHT 
	logging.info("Initializing Exhaust Gas Temp (EGT)")
	try:
		egt = TempSensor(board.D6)
	except RuntimeError as e:
		logging.error("Unable to initialize EGT")
		logging.error(e)

	# Create the speed & position (GPS) 
	logging.info("Initializing GPS")
	from gps import Gps
	gps = Gps()

	# Create the Tach
	logging.info("Initializing Tachometer")
	from tach import Tach
	tach = Tach()

	# Create the Accelerometer
	logging.info("Initializing Accelerometer")
	from accel import Accelerometer
	accelerometer = Accelerometer()

	# Create the clutch
	from clutch import Clutch
	clutch = Clutch()



	print(f'Publishing to topic {ps.topic}')
	logging.info(f'Publishing to topic {ps.topic}')
	#loopCount = 0
	#while loopCount < 1000:
	while True:
		message = { 'device': '63GL', 
			'payload': { 
				'timestamp': str(math.trunc(time.time()*1000)), 
				'gear': gear.gear(), 
				'cht': cht.temperature(), 
				'egt': egt.temperature(), 
				'rpms': tach.rpms(), 
				'throttle': throttle.percent(), 
				'clutch': clutch.in_gear,
				'position': {
					'lat': gps.latitude(), 
					'long': gps.longitude(), 
					'altitude': gps.altitude()
				},
				'speed': gps.speed(),
				'acceleration': {
					'x': accelerometer.x(),
					'y': accelerometer.y(),
					'z': accelerometer.z()
				}
			} 
		}
		ps.publish(message)
		#print( "Published topic "+ps.topic + " " + str(message) )
		#loopCount += 1
		#time.sleep(.2)
		time.sleep(.2)
	print
