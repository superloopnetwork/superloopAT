from baseplatform import BasePlatform
from baseinterface import BaseInterface

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

