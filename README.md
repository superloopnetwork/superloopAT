# ntwautotools
Network Automation Tools

This Python application is in progress but currently provides network automation of running configuration backups from common vendors. 

The supported vendors include the following:

1. Cisco Systems
2. Arista Neworks
3. Juniper Networks
4. Brocade Communications Systems

Simply create a text file and name it 'master_device_list' with the device information populated like so:

[ip_address],[hostname],[username],[password],[vendor],[type]

There are a total of 6 fields seperated by the delimiter comma ','.

[ip_address] - ip address of the device; [hostname] - hostname of device; [username] - username to log into device; [password] - password to log into device (encrypted in base64 format); [vendor] - vendor name in small letters; current support vendors are, 'cisco','arista','juniper','brocade'; if other vendors are used, the application will still accept it but will create an unknown object type; [type] - type of device; 'router', 'switch', 'firewall', etc...

Here is an example:

10.20.30.40,core.rt.superloop.sfo,admin,YmxhaGJsYWhibGFo,cisco,router

Execute the application via 'python ntw_auto_tools.py'. Hit '1' to view the loaded device/object in memory and '2' to perform running config backup.

Configurations are backed up in the /configs/ directory.

More automation features to come...

Enjoy!
