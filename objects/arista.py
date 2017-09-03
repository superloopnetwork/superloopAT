########################## ARISTA CLASS ##########################

from initialize import Initialize

class AristaPlatform(Initialize):

	
    def show_config(self):
		f = open("/configs/%s" % self.ip, "w")
		output = self.net_connect.send_command("show running-config")
		print output
		f.write(output)
		f.close()	
	

