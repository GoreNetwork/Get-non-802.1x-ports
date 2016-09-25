import os
import re
import socket
import sys
import netmiko
import time
def no_inital_space(line):
    if line[0] == "#":
        return line[1:]
    else:
        return line
def no_extra_spaces(line):

	lst = ""
	for each_letter in line:
		if each_letter != " ":
			lst=lst+each_letter
		if each_letter == " ":
			lst=lst+"#"
	for pound in lst:
		lst = lst.replace("##", "#")
	return lst

def remove_return(entry):
	tmp = entry.rstrip('\n')
	return tmp
	
device_to_check = []
def read_in_switches(input):
	for line in open(input, 'r').readlines():
		device_to_check.append(line)
#Looks for the list of switches in a file in the same folder called switches (no extension)
switches_list = 'switches'
read_in_switches(switches_list)
No_nac = False
commands = ['show run | s nterface']
#These are the lines it's looking for to see if the port shouldn't be NACed
dont_nac_this = ["violation restrict","nterface Vlan",'ip address',"passive-interface","tacacs","mls netflow","source-interface","TenGigabitEthernet","mode trunk",'collect interface']
for ip in device_to_check:
	print (ip)
	ip = remove_return(ip)
	try:
#put in your username and password here
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username='your username', password='your password') 
		for command in commands:
			output = net_connect.send_command(command)
			for int_line in output.split("\n"):
#If line says "nterface" it assumes it's a new interface and assumes it doesn't have NAC on it.			
				if "nterface" in int_line:
					if No_nac == True:
						print(interface)
					interface = int_line
					No_nac=True
#Here it runs though the commands that says "This does have NAC on it, or it doesn't need it" so if a line in the dont_nac_this list matches this line it won't show up in the output.					
				for each in dont_nac_this:
					if each in int_line:
						No_nac=False
	except:	
		print ("didn't work... it did not work :-(")