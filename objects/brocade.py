######################### BROCADE CLASS ##########################

from initialize import Initialize

class BrocadePlatform(Initialize):

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
