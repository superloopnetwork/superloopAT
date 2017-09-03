
Network Automation Tools
Disclaimer: code may need to be modified to according to environment. Free feel to contact me for any assistance - wailit@gmail.com

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

Execute the application via 'python main.py'. Hit '1' to view the loaded device/object in memory and '2' to perform running config backup.

Configurations are backed up in the /configs/ directory.

Switchport interface configuration has now been implemented. This feature allows you to store the configuration of switchports in a file (no limit) and easily mass deploy them via the multithread engine. It's a luxury feature for all environment especially for large scale networks. The application is intelligent enough to prevent any human error in overwriting any live ports in the environment; if the switchport status is 'up' or 'notconnected', configs will not be deployed on those port(s). When the switchport status is in a 'down' state, in other words - administratively down, only then will it be deemed safe and the configs be deployed. 

Simply create a text file and name it whatever you wish with the device information populated like so:

[switch_ip],[interface],[mode],[vlan],[description],[state],[vendor],[type]

There are a total of 8 fields seperated by the delimiter comma ','.

[switch_ip] - ip address of the device; [interface] - switchport interface you are configuring. you must type out the full interface name and not it's abbreviated form. for example, 'GigabitEthernet1/0/1' instead of 'Gi1/0/1'; [mode] - mode of switchport, either 'access' or 'trunk'; [vlan] - vlan number that you want the access port to be on. if it's configured as trunk, a single number will yeild a native vlan, if you want to trunk all vlans, set the value to 'all'; [description] - description of switchport; [state] - the state of the switchport you would like it to be in. 'up' or 'down'. [vendor] - current support vendors are, 'cisco','arista','juniper','brocade'; if other vendors are used, the application will still accept it but will create an unknown object type; [type] - type of device; 'router', 'switch', 'firewall', etc...

10.20.30.40,GigabitEthernet1/0/1,access,50,CONNEX: THIS IS AN ACCESS PORT ON VLAN 50 WITH NO SHUTDOWN,up,cisco,switch
10.20.30.40,GigabitEthernet1/0/2,access,30,CONNEX: THIS IS AN ACCESS PORT ON VLAN 30 WITH SHUTDOWN,down,cisco,switch
10.20.30.40,GigabitEthernet1/0/23,trunk,all,CONNEX: THIS IS A TRUNK PORT TRUNKING ALL VLANS WITH NO SHUTDOWN,up,cisco,switch
10.20.30.40,GigabitEthernet1/0/24,trunk,80,CONNEX: THIS IS A TRUNK PORT WITH VLAN 80 AS NATIVE WITH SHUTDOWN,down,cisco,switch

Enjoy!
