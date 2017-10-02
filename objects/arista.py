########################## ARISTA CLASS ##########################

from initialize import Initialize

class AristaPlatform(Initialize):

	def show_config(self):
		f = open("/configs/%s" % self.ip, "w")
		output = self.net_connect.send_command("show running-config")
		print output
		f.write(output)
		f.close()	

	def switchport_config(self,credentials,*arg): 

		if (self.type == 'switch' and self.mode == 'access' and self.state == 'up'): 
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport access vlan %s' % self.vlan,'description %s' % self.description,'spanning-tree portfast','spanning-tree bpduguard enable','no shutdown'] 
		elif (self.type == 'switch' and self.mode == 'access' and self.state == 'down'): 
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport access vlan %s' % self.vlan,'description %s' % self.description,'spanning-tree portfast','spanning-tree bpduguard enable','shutdown'] 
		elif (self.type == 'switch' and self.mode == 'trunk' and self.vlan == 'all' and self.state == 'up'): 
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport trunk allowed vlan all','description %s' % self.description,'no shutdown'] 
		elif (self.type == 'switch' and self.mode == 'trunk' and self.vlan == 'all' and self.state == 'down'): 
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport trunk allowed vlan all','description %s' % self.description,'shutdown'] 
		elif (self.type == 'switch' and self.mode == 'trunk' and self.state == 'up'): 
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport trunk native vlan %s' % self.vlan,'description %s' % self.description,'no shutdown'] 
		elif (self.type == 'switch' and self.mode == 'trunk' and self.state == 'down'): 
			commands = ['interface %s' % self.interface,'switchport mode %s' % self.mode,'switchport trunk native vlan %s' % self.vlan,'description %s' % self.description,'shutdown'] 
		 
		self.connect_interface(credentials) 
		output = self.net_connect.enable() 
		print('#' * 86) 

		if self.arista_check_interface_status(): 
			output = self.net_connect.send_config_set(commands) 
			print output 
		else: 
			print ('!! INTERFACE %s ON HOST %s IS NOT ADMINISTRATIVELY SHUTDOWN. CONFIGURATIONS WILL NOT BE APPLIED !!' % (self.interface,self.switchip)) 

		print('#' * 86) 
		self.net_connect.disconnect() 

	def add_credentials(self,credentials,*args):
        
		if (self.type == 'switch'):
			commands = ['username %s privilege 15 secret %s' % (credentials[0],credentials[1])]
		
		self.connect()
		print('#' * 86)
		output = self.net_connect.enable()
		output = self.net_connect.send_config_set(commands)
		print output
		print('#' * 86)
		self.net_connect.disconnect()
