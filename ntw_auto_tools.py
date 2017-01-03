#!/usr/bin/env/python

import re
import paramiko
import time
import base64
import datetime
import os

ntw_device = []										# GLOBAL VARIABLE OF NTW_DEVICE OF TYPE LIST

class BasePlatform(object):

 def __init__(self,ip,hostname,username,password,vendor,type):
   self.ip = ip
   self.hostname = hostname
   self.username = username
   self.password = password
   self.vendor = vendor
   self.type = type
   self.client = paramiko.SSHClient()
   self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   self.session = None

 def connect(self):
   password = base64.b64decode(self.password)
   self.client.connect(self.ip,username=self.username,password=password,look_for_keys=False, allow_agent=False)
   self.session = self.client.invoke_shell()

########################## CISCO CLASS ##########################

class CiscoPlatform(BasePlatform):

 def disable_paging(self):
   self.session.send("terminal length 0\n")

 def config_backup(self):
   f = open("/configs/%s" % self.ip, "w")
   self.session.send("\n")
   self.session.send("show run\n")
   time.sleep(1)
   output = self.session.recv(10000)
   print output
   f.write(output)
   f.close()

 def show_interface_status(self):
   self.session.send("\n")
   self.session.send("show interface status\n")
   time.sleep(1)
   output = self.session.recv(10000)
   print output
   f.write(output)
   f.close()

 def show_ip_arp(self,ip_address):
   remote_conn.send("\n")
   remote_conn.send("show ip arp | include %s\n" % ip_address)
   time.sleep(1)

########################## ARISTA CLASS ##########################

class AristaPlatform(object):

 def disable_paging(self):
   self.session.send("terminal length 0\n")
   time.sleep(1)

 def config_backup(self):
   f = open("%s" % self.ip, "w")
   self.session.send("\n")
   self.session.send("show run\n")
   time.sleep(3)
   output = self.session.recv(65535)
   print output
   f.write(output)
   f.close()

########################## JUNIPER CLASS ##########################

class JuniperPlatform(object):

 def disable_paging(self):
   self.session.send("set cli screen-length 0\n")

 def config_backup(self):
   f = open("%s" % self.ip, "w")
   self.session.send("\n")
   self.session.send("show configuration | display set\n")
   time.sleep(2)
   output = self.session.recv(65535)
   print output
   f.write(output)
   f.close()
   
########################## BROCADE CLASS ##########################

class BrocadePlatform(object):

 def disable_paging(self):
   time.sleep(2)
   self.session.send("terminal length 0\n")

 def config_backup(self):
   f = open("%s" % self.ip, "w")
   self.session.send("show run\n")
   time.sleep(26)
   output = self.session.recv(65535)
   print output
   f.write(output)
   f.close()

########################## CITRIX CLASS ##########################

class CitrixPlatform(object):

 pass

########################## UBUNTU CLASS ##########################

class UbuntuPlatform(object):

 pass

########################## UNKNOWN CLASS ##########################

class UnknownPlatform(object):           
 
 pass

########################## FUNCTIONS ##########################

def config_backup():
 #THIS FUNCTION CREATE RUNNING CONFIGURATION BACKUP
 
 start_time = datetime.datetime.now()

 index = 0

 for i in ntw_device:
   ntw_device[index].connect()
   ntw_device[index].disable_paging()
   ntw_device[index].config_backup()
   
   index = index + 1

 print("\n")
 print("TIME ELAPSED: {}\n".format(datetime.datetime.now() - start_time))

def view_devices():

 index = 0
 counter = 1

 print("######################### NTW DEVICE LIST #########################\n")
 for i in ntw_device:
   if (counter < 10):
     print "%s.  %-19s %s" % (counter,ntw_device[index].ip,ntw_device[index].hostname)
   if (counter >= 10):
     print "%-1s. %-19s %s" % (counter,ntw_device[index].ip,ntw_device[index].hostname)
   index = index + 1
   counter = counter + 1
 print("\n")

def add_devices():
 print("This is the view device function")


def read_device_list():										# THIS FUNCTION READS THE DEVICE_LIST.TXT AND POPULATES THE LIST OF OBJECTS FOR EACH DEVICE

 f = open("device_list.txt")
 init_list = f.readlines()

 for i in init_list:
   strip_list = i.strip("\n")
   list = strip_list.split(",")

   if (list[4] == 'cisco'):
     device = CiscoPlatform(list[0],list[1],list[2],list[3],list[4],list[5]) 
     ntw_device.append(device)

   elif (list[4] == 'arista'):
     device = AristaPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
     ntw_device.append(device)

   elif (list[4] == 'juniper'):
     device = JuniperPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
     ntw_device.append(device)

   elif (list[4] == 'brocade'):
     device = BrocadePlatform(list[0],list[1],list[2],list[3],list[4],list[5])
     ntw_device.append(device)

   elif (list[4] == 'citrix'):
     device = CitrixPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
     ntw_device.append(device)

   elif (list[4] == 'ubuntu'):
     device = UbuntuPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
     ntw_device.append(device)

   else:
     device =UnknownPlatform(list[0],list[1],list[2],list[3],list[4],list[5])
     ntw_device.append(device) 
     print "!%s IS A NON SUPPORTED DEVICE. UNKNOWN OBJECT HAS BEEN CREATED!" % list[1]


def main():

 os.system('clear')
 mainmenu = {1: view_devices,2: config_backup}		
 # THIS IS THE DICTIONARY OF THE MAINMENU

 read_device_list()
                   
 selection = 0

 while (selection !=3):
  print("##################### NETWORK AUTOMATION TOOLS ####################\n")
  print("1. VIEW DEVICE LIST")
  print("2. CONFIGURATION BACKUP")
  print("3. EXIT TO SHELL")
  print("\n")
  selection = int(raw_input("PLEASE MAKE YOUR SELECTION: "))
  print("\n") 
  if (selection >= 0) and (selection < 3):
	mainmenu[selection]()


if __name__ == "__main__":
 main()
