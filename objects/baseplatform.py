######################### BASE CLASSES ###########################

from netmiko import ConnectHandler
import base64


class BasePlatform(object):

	def __init__(self,ip,hostname,username,password,vendor,type):
		self.ip = ip
   		self.hostname = hostname
   		self.username = username
   		self.password = password
   		self.vendor = vendor
   		self.type = type
		self.password_decrypt= base64.b64decode(self.password)

	def connect(self):
		self.net_connect = ConnectHandler(self.ip,self.hostname,self.username,self.password_decrypt,self.secret(),device_type=self.device_call())
			
	def secret(self):
		enable_secret = ''
		if (self.location() == 'wdstk'):
			enable_secret = base64.b64decode(self.password)
		elif (self.location() == 'ktch'):
			enable_secret = base64.b64decode(self.password)

		return enable_secret
		
	def location(self):
		datacenter_location = ''
		if (self.type == 'firewall'):
			location_list = self.hostname.split('-')	
			datacenter_location = location_list[3]

		elif (self.type == 'switch' or self.type == 'router'):
			location_list = self.hostname.split('.')	
			datacenter_location = location_list[3]

		return datacenter_location

	def device_call(self):
		device_attribute = ''
		if (self.type == 'router' or self.type == 'switch'):
			device_attribute = 'cisco_ios'
		
		elif (self.type == 'firewall'):
			device_attribute = 'cisco_asa'

		return device_attribute

