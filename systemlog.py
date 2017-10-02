######################## FUNCTIONS ##############################

from multithread import multithread_engine
import initialize

def syslog_config():

	controller = 'syslog_config'
	multithread_engine(initialize.ntw_device,controller,initialize.credentials)
