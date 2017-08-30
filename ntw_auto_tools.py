#!/usr/bin/env/python

from netmiko import ConnectHandler
from view import view_devices
from view import view_interfaces
import threading 
import re
import getpass 
import time
import base64
import datetime
import os

ntw_device = []
switchport = []
credentials = []
process = True
# GLOBAL VARIABLE OF NTW_DEVICE & SWITCHPORT OF TYPE LIST


######################### BASE CLASSES ###########################
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

class BaseInterface(object):

	def __init__(self,switchip,interface,mode,vlan,description,state,vendor,type):  
		self.switchip = switchip
		self.interface = interface
		self.mode = mode
		self.vlan = vlan
		self.description = description
		self.state = state
		self.vendor = vendor
		self.type = type
	
	def connect_interface(self,credentials):
		self.net_connect = ConnectHandler(self.switchip,None,credentials[0],credentials[1],credentials[1],port=65500,device_type=self.device_call())

	def cisco_interface_notation(self):
		notation = self.interface.split('GigabitEthernet')[1]
		
		return notation
		
	def cisco_check_interface_status(self):
		interface_status = self.net_connect.send_command('show interface status | include %s' % self.cisco_interface_notation())
		list = interface_status.split('\n')[0]
		list = list.split()
		for element in list:
			if element == 'disabled':
				execute = True
				break
			elif element == 'notconnect':
				execute = False
			else:
				execute = False

		return execute

########################## INIT. CLASS ###########################

class Initialize(BasePlatform,BaseInterface):

	def __init__(self,*arg):
		if (len(arg) == 6):
			ip,hostname,username,password,vendor,type = arg
			BasePlatform.__init__(self,ip,hostname,username,password,vendor,type)
		elif (len(arg) == 8):
			switchip,interface,mode,vlan,description,state,vendor,type = arg
			BaseInterface.__init__(self,switchip,interface,mode,vlan,description,state,vendor,type)
		else:
			raise ValueError('Inconsistent arguments number')

########################## CISCO CLASS ###########################

class CiscoPlatform(Initialize):

	def config_backup(self,*args):

		change_type = 'global'
		f = open("/configs/%s" % self.ip, "w")
		self.connect()
		print('#' * 86)
		output = self.net_connect.send_command_expect("show running-config")
		print output
		f.write(output)
		f.close()
		print('#' * 86)
		self.net_connect.disconnect()

	def syslog_config(self,*args):
		

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

	def switchport_config(self,credentials,*args):

		if (self.type == 'switch' and self.mode == 'access' and self.state == 'up'):
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport access vlan %s' % self.vlan,'description %s' % self.description,'spanning-tree portfast','spanning-tree bpduguard enable','no shutdown']
		elif (self.type == 'switch' and self.mode == 'access' and self.state == 'down'):
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport access vlan %s' % self.vlan,'description %s' % self.description,'spanning-tree portfast','spanning-tree bpduguard enable','shutdown']
		elif (self.type == 'switch' and self.mode == 'trunk' and self.vlan == 'all' and self.state == 'up'):
			commands = ['interface %s' % self.interface,'switchport trunk encapsulation dot1q','switchport mode %s' % self.mode,'switchport trunk allowed vlan all','description %s' % self.description,'no shutdown']
		elif (self.type == 'switch' and self.mode == 'trunk' and self.vlan == 'all' and self.state == 'down'):
			commands = ['interface %s' % self.interface,'switchport trunk encapsulation dot1q','switchport mode %s' % self.mode,'switchport trunk allowed vlan all','description %s' % self.description,'shutdown']
		elif (self.type == 'switch' and self.mode == 'trunk' and self.state == 'up'):
			commands = ['interface %s' % self.interface,'switchport trunk encapsulation dot1q','switchport mode %s' % self.mode,'switchport trunk native vlan %s' % self.vlan,'description %s' % self.description,'no shutdown']
		elif (self.type == 'switch' and self.mode == 'trunk' and self.state == 'down'):
			commands = ['interface %s' % self.interface,'switchport trunk encapsulation dot1q','switchport mode %s' % self.mode,'switchport trunk native vlan %s' % self.vlan,'description %s' % self.description,'shutdown']

		self.connect_interface(credentials)
		print('#' * 86)
		if self.cisco_check_interface_status():
			output = self.net_connect.send_config_set(commands)
			print output
		else:
			print ('!! INTERFACE %s ON HOST %s IS NOT ADMINISTRATIVELY SHUTDOWN. CONFIGURATIONS WILL NOT BE APPLIED !!' % (self.interface,self.switchip))
		print('#' * 86)
		self.net_connect.disconnect()


########################## ARISTA CLASS ##########################

class AristaPlatform(Initialize):

	
    def show_config(self):
		f = open("/configs/%s" % self.ip, "w")
		output = self.net_connect.send_command("show running-config")
		print output
		f.write(output)
		f.close()	
	

######################### JUNIPER CLASS ##########################

class JuniperPlatform(Initialize):

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

class BrocadePlatform(Initialize):

	pass

########################## CITRIX CLASS ##########################

class CitrixPlatform(Initialize):

	pass

########################## UBUNTU CLASS ##########################

class UbuntuPlatform(Initialize):

	pass

######################### UNKNOWN CLASS ##########################

class UnknownPlatform(Initialize): 
 
	pass


######################## FUNCTIONS ##############################

def switchport_config(database):


	global switchport
	global credentials
	del switchport[:]
	del credentials[:]
	check = 'interface_list'
	controller = 'switchport_config'
	process_engine(database,check)
	view_interfaces(switchport)
#	switchport.check_interface_status()
	username = raw_input('PLEASE ENTER YOUR USERNAME: ')
	credentials.append(username)
	password = getpass.getpass(prompt="PLEASE ENTER YOUR PASSWORD: ")
	credentials.append(password)
	multithread_engine(switchport,controller,credentials)


####################### ENGINE FUNCTIONS ########################

def multithread_engine(object,redirect,credentials):
	
	start_time = datetime.datetime.now()
	index = 0

	if(object == ntw_device):
		arguments = None
	if(object == switchport):
		arguments = credentials
	for i in object:
		my_thread = threading.Thread(target=getattr(object[index],redirect) , args=(arguments,))
		my_thread.start()

		index = index + 1

	main_thread = threading.currentThread()
	for some_thread in threading.enumerate():
		if some_thread != main_thread:
			print(some_thread)
			some_thread.join()

	print("\n")
	print("TIME ELAPSED: {}\n".format(datetime.datetime.now() - start_time))



def process_engine(database,check):
# THIS FUNCTION READS THE MASTER_DEVICE_LIST AND POPULATES THE LIST OF OBJECTS FOR EACH DEVICE

	f = open(database)
	init_list = f.readlines()
	
	if (check == 'device_list'):

		for i in init_list:
			strip_list = i.strip('\n')
			list = strip_list.split(',')
			
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
				device = UnknownPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				ntw_device.append(device) 
				print "!%s IS A NON SUPPORTED DEVICE. UNKNOWN OBJECT HAS BEEN CREATED!" % list[1]
	
	elif (check == 'interface_list'):

		for i in init_list:
			strip_list = i.strip('\n')
			list = strip_list.split(',')

			
			if (list[6] == 'cisco'):
				interface = CiscoPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7]) 
				switchport.append(interface)
	
			elif (list[6] == 'arista'):
				interface = AristaPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				switchport.append(interface)
	
			elif (list[6] == 'juniper'):
				interface = JuniperPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				switchport.append(interface)
	
			elif (list[6] == 'brocade'):
				interface = BrocadePlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				switchport.append(interface)
	
			elif (list[6] == 'citrix'):
				interface = CitrixPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				switchport.append(interface)
	
			elif (list[6] == 'ubuntu'):
				interface = UbuntuPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				switchport.append(interface)
			else:
				interface = UnknownPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				switchport.append(interface) 
				print "!%s IS A NON SUPPORTED DEVICE. UNKNOWN OBJECT HAS BEEN CREATED!" % list[1]

############################ MENU SCREENS ############################

def main():

		os.system('clear')

		global process		

		if (process == True):
			database = 'master_device_list'
			check = 'device_list'
			process_engine(database,check)
			process = False

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

			if selection == 1:
				view_devices(ntw_device)

			elif selection == 2:
				controller = 'config_backup'
				multithread_engine(ntw_device,controller,credentials)
			
			elif selection == 3:
				execute_change()

			elif selection == 4:
				loop = False

			else:
				raw_input("! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n")

def global_config():

	selection = 0

	while (selection !=4):
		print '#' * 19, 'CONFIG CENTER > EXECUTE CHANGE > GLOBAL CHANGE', '#' * 19, '\n'
		print '1. ADD/REMOVE CREDENTIALS'
  		print '2. SNMP CONFIGURATION'
  		print '3. SYSLOG CONFIGURATION'
  		print '4. RETURN TO EXECUTE CHANGE MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print("\n")

		if selection == 3:
			controller = 'syslog_config'
			multithread_engine(ntw_device,controller,credentials)
		elif selection == 4:
			loop = False
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
  		print '4. RETURN TO MAIN MENU'
  		print '\n'
  		selection = int(raw_input('PLEASE MAKE YOUR SELECTION: '))
  		print'\n'
		
		if selection == 1:
			global_config()
		elif selection == 2:
				database = raw_input('PLEASE INPUT THE FILENAME TO IMPORT: ')
				print
				switchport_config(database)
		elif selection == 4:
			loop = False

		else:
			raw_input("! ! ! ! INVALID SELECTION. PLEASE TRY AGAIN ! ! ! !\n")


if __name__ == '__main__':
	main()
