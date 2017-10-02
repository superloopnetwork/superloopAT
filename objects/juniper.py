######################### JUNIPER CLASS ##########################

from initialize import Initialize

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

		self.connect_interface()
		print('#' * 86)
		output = self.net_connect.send_config_set(commands)
		print output
		print('#' * 86)
		self.net_connect.disconnect()

	def add_credentials(self,credentials,*args):

		if (self.type == 'router' or self.type == 'switch' or self.type == 'firewall'):
			commands = ['set system login user %s class super-user' % credentials[0],'set system login user %s authentication plain-text-password' % credentials[0],'%s' % credentials[1],'%s' % credentials[1]]

		self.connect()
		print('#' * 86)
		output = self.net_connect.enable()
		output = self.net_connect.send_config_set(commands)
		self.net_connect.commit(and_quit=True)
		print output
		print('#' * 86)
		self.net_connect.disconnect()

	def rm_credentials(self,credentials,*args):
		
		if (self.type == 'router' or self.type == 'switch' or self.type == 'firewall'):
			commands = ['del system login user %s' % credentials[0]]

		self.connect()
		print('#' * 86)
		output = self.net_connect.enable()
		output = self.net_connect.send_config_set(commands)
		self.net_connect.commit(and_quit=True)
		print output
		print('#' * 86)
		self.net_connect.disconnect()

