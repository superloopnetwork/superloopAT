####################### ENGINE FUNCTIONS ########################

from objects.cisco import CiscoPlatform
from objects.arista import AristaPlatform
from objects.juniper import JuniperPlatform
from objects.brocade import BrocadePlatform
from objects.citrix import CitrixPlatform
from objects.ubuntu import UbuntuPlatform
from objects.unknown import UnknownPlatform
import initialize

def parse_engine(database,check):
# THIS FUNCTION READS THE MASTER_DEVICE_LIST AND POPULATES THE LIST OF OBJECTS FOR EACH DEVICE

	f = open(database)
	init_list = f.readlines()
	
	if (check == 'device_list'):

		for i in init_list:
			strip_list = i.strip('\n')
			list = strip_list.split(',')
			
			if (list[4] == 'cisco'):
				device = CiscoPlatform(list[0],list[1],list[2],list[3],list[4],list[5]) 
				initialize.ntw_device.append(device)
	
			elif (list[4] == 'arista'):
				device = AristaPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				initialize.ntw_device.append(device)
	
			elif (list[4] == 'juniper'):
				device = JuniperPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				initialize.ntw_device.append(device)
	
			elif (list[4] == 'brocade'):
				device = BrocadePlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				initialize.ntw_device.append(device)
	
			elif (list[4] == 'citrix'):
				device = CitrixPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				initialize.ntw_device.append(device)
	
			elif (list[4] == 'ubuntu'):
				device = UbuntuPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				initialize.ntw_device.append(device)
			else:
				device = UnknownPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
				initialize.ntw_device.append(device) 
				print "!%s IS A NON SUPPORTED DEVICE. UNKNOWN OBJECT HAS BEEN CREATED!" % list[1]
	
	elif (check == 'interface_list'):

		for i in init_list:
			strip_list = i.strip('\n')
			list = strip_list.split(',')

			
			if (list[6] == 'cisco'):
				interface = CiscoPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7]) 
				initialize.switchport.append(interface)
	
			elif (list[6] == 'arista'):
				interface = AristaPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				initialize.switchport.append(interface)
	
			elif (list[6] == 'juniper'):
				interface = JuniperPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				initialize.switchport.append(interface)
	
			elif (list[6] == 'brocade'):
				interface = BrocadePlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				initialize.switchport.append(interface)
	
			elif (list[6] == 'citrix'):
				interface = CitrixPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				initialize.switchport.append(interface)
	
			elif (list[6] == 'ubuntu'):
				interface = UbuntuPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				initialize.switchport.append(interface)
			else:
				interface = UnknownPlatform(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7])
				initialize.switchport.append(interface) 
				print "!%s IS A NON SUPPORTED DEVICE. UNKNOWN OBJECT HAS BEEN CREATED!" % list[1]

