########################## CISCO CLASS ###########################

from initialize import Initialize

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

