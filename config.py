######################## FUNCTIONS ##############################
from multithread import multithread_engine
import initialize

def config_backup():
	controller = 'config_backup'
	multithread_engine(initialize.ntw_device,controller,initialize.credentials)
