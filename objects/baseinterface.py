from netmiko import ConnectHandler

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

	def arista_interface_notation(self):
		notation = self.interface.split('Ethernet')[1]
		
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

	def arista_check_interface_status(self):
		interface_status = self.net_connect.send_command('show interface status | include Et%s' % self.arista_interface_notation())
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

