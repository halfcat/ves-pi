#!/usr/bin/env python3

import gpsd as gps_daemon

class Gps:
	"""This is a trivial wrapper around Gpsd.

	"""  
	
	gpsd = None

	def __init__(self):
		self.gpsd = gps_daemon
		self.gpsd.connect()

	def gps(self) -> gps_daemon:
		return self.gpsd

	def has_fix(self) -> bool:
		return self.gpsd.get_current().mode >= 2

	def speed(self) -> float:
		"""Get current speed in MPH or -1 if no GPS fix"""
		if not self.has_fix():
			return -1
		return self.gpsd.get_current().speed()

	def position(self):
		if not self.has_fix():
			return -1
		return self.gpsd.get_current().position_precision()

	def latitude(self) -> float:
		"""Get current latitude in degrees or -1 if no GPS fix"""
		if not self.has_fix():
			return -1
		return self.gpsd.get_current().lat

	def longitude(self) -> float:
		"""Get current longitude in degrees or -1 if no GPS fix"""
		if not self.has_fix():
			return -1
		return self.gpsd.get_current().lon

	def altitude(self) -> float:
		"""Get current altitude in feet(?) or -1 if no GPS fix"""
		if not self.has_fix():
			return -1
		return self.gpsd.get_current().alt

	def get_current(self):
		return self.gpsd.get_current()

if __name__ == '__main__':
	gps = Gps()
	# Get gps position
	packet = gps.get_current()

	# See the inline docs for GpsResponse for the available data
	print(" ************ PROPERTIES ************* ")
	print("  Mode: " + str(packet.mode))
	print("Satellites: " + str(packet.sats))
	if packet.mode >= 2:
		print("  Latitude: " + str(packet.lat))
		print(" Longitude: " + str(packet.lon))
		print(" Track: " + str(packet.track))
		print("  Horizontal Speed: " + str(packet.hspeed))
		print(" Time: " + str(packet.time))
		print(" Error: " + str(packet.error))
	else:
		print("  Latitude: NOT AVAILABLE")
		print(" Longitude: NOT AVAILABLE")
		print(" Track: NOT AVAILABLE")
		print("  Horizontal Speed: NOT AVAILABLE")
		print(" Error: NOT AVAILABLE")

	if packet.mode >= 3:
		print("  Altitude: " + str(packet.alt))
		print(" Climb: " + str(packet.climb))
	else:
		print("  Altitude: NOT AVAILABLE")
		print(" Climb: NOT AVAILABLE")

	print(" ************** METHODS ************** ")
	if packet.mode >= 2:
		print("  Location: " + str(packet.position()))
		print(" Speed: " + str(packet.speed()))
		print("Position Precision: " + str(packet.position_precision()))
		#print("  Time UTC: " + str(packet.time_utc()))
		#print("Time Local: " + str(packet.time_local()))
		print("   Map URL: " + str(packet.map_url()))
	else:
		print("  Location: NOT AVAILABLE")
		print(" Speed: NOT AVAILABLE")
		print("Position Precision: NOT AVAILABLE")
		print("  Time UTC: NOT AVAILABLE")
		print("Time Local: NOT AVAILABLE")
		print("   Map URL: NOT AVAILABLE")

	if packet.mode >= 3:
		print("  Altitude: " + str(packet.altitude()))
		# print("  Movement: " + str(packet.movement()))
		# print("  Speed Vertical: " + str(packet.speed_vertical()))
	else:
		print("  Altitude: NOT AVAILABLE")
		# print("  Movement: NOT AVAILABLE")
		# print(" Speed Vertical: NOT AVAILABLE")

	print(" ************* FUNCTIONS ************* ")
	print("Device: " + str(gpsd.device()))

