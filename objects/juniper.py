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

