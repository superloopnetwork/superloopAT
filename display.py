def view_devices(ntw_device):

	index = 0
	counter = 1
	
	print '#' * 31, 'NETWORK INVENTORY LIST', '#' * 31, '\n'
	for i in ntw_device:
		if (counter < 10):
			print '%s.  %-19s %s' % (counter,ntw_device[index].ip,ntw_device[index].hostname)
		if (counter >= 10):
			print '%-1s. %-19s %s' % (counter,ntw_device[index].ip,ntw_device[index].hostname)
    
		index = index + 1
		counter = counter + 1
    
	print 

def view_interfaces(switchport):

	index = 0
	counter = 1
	
	print
	print '#' * 30, 'INTERFACE CONFIGURATIONS', '#' * 30, '\n'
	for i in switchport:
		if (counter < 10):
			print '%s.  %-19s %-28s %-13s %s' % (counter,switchport[index].switchip,switchport[index].interface,switchport[index].mode,switchport[index].vlan)
		if (counter >= 10):
			print '%-1s. %-19s %-28s %-13s %s' % (counter,switchport[index].switchip,switchport[index].interface,switchport[index].mode,switchport[index].vlan)
    
		index = index + 1
		counter = counter + 1
    
	print 
