#!/usr/bin/env/python

from netmiko import ConnectHandler
import threading 
import re
import paramiko
import time
import base64
import datetime
import os

ntw_device = []
# GLOBAL VARIABLE OF NTW_DEVICE OF TYPE LIST


########################## BASE CLASS ###########################
class BasePlatform(object):

	def __init__(self,ip,hostname,username,password,vendor,type):
		self.ip = ip
   		self.hostname = hostname
   		self.username = username
   		self.password = password
   		self.vendor = vendor
   		self.type = type
		self.decrypt_password = base64.b64decode(self.password)

	def connect(self):
		self.net_connect = ConnectHandler(self.ip,self.hostname,self.username,self.decrypt_password,self.secret(),device_type=self.device_call())

	def secret(self):
		enable_secret = ''
		if (self.location() == 'wdstk'):
			enable_secret = base64.b64decode(self.password)
		elif (self.location() == 'ktch'):
			enable_secret = base64.b64decode(self.password)

		return enable_secret
		
	def location(self):
		if (self.type == 'firewall'):
			location_list = self.hostname.split('-')	
			datacenter_location = location_list[3]

		elif (self.type == 'switch' or self.type == 'router'):
			location_list = self.hostname.split('.')	
			datacenter_location = location_list[3]

		return datacenter_location

	def device_call(self):
		if (self.type == 'router' or self.type == 'switch'):
			device_attribute = 'cisco_ios'
		
		elif (self.type == 'firewall'):
			device_attribute = 'cisco_asa'

		return device_attribute
		
########################## CISCO CLASS ###########################

class CiscoPlatform(BasePlatform):

	def config_backup(self):

		f = open("/configs/%s" % self.ip, "w")
		self.connect()
		print('#' * 86)
		output = self.net_connect.send_command_expect("show running-config")
		print output
		f.write(output)
		f.close()
		print('#' * 86)
		self.net_connect.disconnect()

	def syslog_config(self):

		if (self.type == 'router' or self.type == 'switch'):
			commands = ['logging 10.50.30.2']
		
		elif (self.type == 'firewall'):
			commands = ['logging host inside 10.50.30.2']

		self.connect() 
		print('#' * 86)
		output = self.net_connect.send_config_set(commands)
		print output
		print('#' * 86)
		self.net_connect.disconnect()

########################## ARISTA CLASS ##########################

class AristaPlatform(object):

	
    def show_config(self):
		f = open("/configs/%s" % self.ip, "w")
		output = self.net_connect.send_command("show running-config")
		print output
		f.write(output)
		f.close()	
	

######################### JUNIPER CLASS ##########################

class JuniperPlatform(object):

	def config_backup(self):
		f = open("/configs/%s" % self.ip, "w")
	
		self.connect()
		print()
		print('#' * 83)
		output = self.net_connect.send_command_expect("show configuration | display set")
		print output
		f.write(output)
		f.close()
		print('#' * 83)
		self.net_connect.disconnect()
		print()

######################### BROCADE CLASS ##########################

class BrocadePlatform(object):

	pass

########################## CITRIX CLASS ##########################

class CitrixPlatform(object):

	pass

########################## UBUNTU CLASS ##########################

class UbuntuPlatform(object):

	pass

######################### UNKNOWN CLASS ##########################

class UnknownPlatform(object):           
 
	pass

########################### FUNCTIONS ############################

def view_devices():

	index = 0
	counter = 1

	print '#' * 31, 'NETWORK INVENTORY LIST', '#' * 31, '\n'
	for i in ntw_device:
		if (counter < 10):
			print "%s.  %-19s %s" % (counter,ntw_device[index].ip,ntw_device[index].hostname)
		if (counter >= 10):
			print "%-1s. %-19s %s" % (counter,ntw_device[index].ip,ntw_device[index].hostname)
   	
		index = index + 1
   		counter = counter + 1
 	
	print 


def multithread_engine(redirect):
	
	start_time = datetime.datetime.now()

	index = 0

	for i in ntw_device:
		my_thread = threading.Thread(target=getattr(ntw_device[index],redirect) , args=())
		my_thread.start()

		index = index + 1

	main_thread = threading.currentThread()
	for some_thread in threading.enumerate():
		if some_thread != main_thread:
			print(some_thread)
			some_thread.join()

	print("\n")
	print("TIME ELAPSED: {}\n".format(datetime.datetime.now() - start_time))



def read_device_list():
# THIS FUNCTION READS THE DEVICE_LIST.TXT AND POPULATES THE LIST OF OBJECTS FOR EACH DEVICE

	f = open("device_list.txt")
	init_list = f.readlines()

	for i in init_list:
		strip_list = i.strip("\n")
		list = strip_list.split(",")
		
		if (list[4] == 'cisco'):
			device = CiscoPlatform(list[0],list[1],list[2],list[3],list[4],list[5]) 
			ntw_device.append(device)

		elif (list[4] == 'arista'):
			device = AristaPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
			ntw_device.append(device)

		elif (list[4] == 'juniper'):
			device = JuniperPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
			ntw_device.append(device)

		elif (list[4] == 'brocade'):
			device = BrocadePlatform(list[0],list[1],list[2],list[3],list[4],list[5])
			ntw_device.append(device)

		elif (list[4] == 'citrix'):
			device = CitrixPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
			ntw_device.append(device)

		elif (list[4] == 'ubuntu'):
			device = UbuntuPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
			ntw_device.append(device)

		else:
			device =UnknownPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
			ntw_device.append(device) 
			print "!%s IS A NON SUPPORTED DEVICE. UNKNOWN OBJECT HAS BEEN CREATED!" % list[1]


############################ MENU SCREENS ############################

def global_config():

	selection = 0

	while (selection !=4):
		print '#' * 19, 'CONFIG CENTER > EXECUTE CHANGE > GLOBAL CHANGE', '#' * 19, '\n'
		print '1. ADD/REMOVE CREDENTIALS'
  		print '2. SNMP CONFIGURATION'
  		print '3. SYSLOG CONFIGURATION'
  		print '4. RETURN TO MAIN MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print("\n")

		if selection == 3:
			controller = 'syslog_config'
			multithread_engine(controller)
		else:
			raw_input('Wrong option selection. Enter any key to try again..')

def execute_change():

	selection = 0

	loop=True

	while loop:
		print '#' * 29, 'MAIN MENU > EXECUTE CHANGE', '#' * 29, '\n'
		print '1. GLOBAL CONFIGURATION'
  		print '2. SWITCHPORT CONFIGURATION'
  		print '3. ROUTED PORT CONFIGURATION'
  		print '4. NEW ARISTA TORS'
  		print '5. RETURN TO MAIN MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print'\n'
		
		if selection==1:
			global_config()

		elif selection==5:
			main()

		else:
			raw_input("! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n")

def main():

		os.system('clear')

		read_device_list()
		
		loop=True
                   
		while loop:
			print '#' * 30, 'NETWORK AUTOMATION TOOLS', '#' * 30, '\n'
  			print '1. VIEW DEVICE LIST'
  			print '2. CONFIGURATION BACKUP'
  			print '3. EXECUTE CHANGE'
  			print '4. EXIT TO SHELL'
  			print '\n'
  			selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  			print '\n' 

			if selection==1:
				view_devices()

			elif selection==2:
				controller = 'config_backup'
				multithread_engine(controller)
			
			elif selection==3:
				controller = 'execute_change'
				execute_change()

			elif selection==4:
				loop=False

			else:
				raw_input("! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n")

if __name__ == '__main__':
	main()
