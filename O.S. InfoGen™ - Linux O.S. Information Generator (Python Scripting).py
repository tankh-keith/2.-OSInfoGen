#!/usr/bin/python3



#i. GET USER INPUTS
name=input("Tell me your name: ")
print('')
print(f"\033[1mHello, {name}.\033[0m")
print('')
print("\033[1mWelcome to O.S. InfoGen™ by Keith Tan.\033[0m")
print("(starting the script in 3 seconds...)")
import time
time.sleep(3)
print('')



#ii. IMPORT MODULES
import platform #to get O.S. information
import netifaces #to get Private IP Address
import requests #to get Public IP Address
import socket #to get Default Gateway IP Address
import psutil #to get hard disk information
import subprocess #to execute shell command 'du' and get top 5 largest directories
import re #to use REGEX to better-display directory results



#iii. DISPLAY O.S. VERSION
print("\033[1mOperating System details:\033[0m")

def display_os_version():
	os_name=platform.system()
	os_ver=platform.version()
	os_verrelease=platform.release()
	os_mach=platform.machine()
	print(f"Operating System: {os_name}")
	print(f"- Version: {os_ver}")
	print(f"- Version Release: {os_verrelease}")
	print(f"- Processor Architecture: {os_mach}")
	
display_os_version()
print('')



#iv. DISPLAY PRIVATE IP ADDRESS, PUBLIC IP ADDRESS, DEFAULT GATEWAY

# Display Private IP address:

def get_private_ip(): #function that gets private IPv4 address of host, using netifaces module
    try:
        for el in netifaces.interfaces(): #look through network interfaces of host machine
            if el != "lo":  # 'lo' represents loopback interface, to ignore it...
                addresslst = netifaces.ifaddresses(el) #extract dictionary of info for each network interface
                if netifaces.AF_INET in addresslst: #check if IPv4 is within dictionary of info, if yes...
                    priv_ip = addresslst[netifaces.AF_INET][0]['addr'] #get the 1st IPv4 address of interface
                    print(priv_ip) #private IP address obtained
        return "No private IP address found."
    except Exception as err:
        return f"Unable to fetch private IP. Error: {err}"
        
print("\033[1mPrivate IP Address:\033[0m")
get_private_ip()
print('')

# Display Public IP address:

def get_public_ip(): #function that gets public IP address of host, using requests module
    try:
		#HTTP GET request to a specific URL that gets info on the host's public IP address:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json() #parse API response (in JSON format), to python dictionary format
        public_ip = data['ip'] #extract value (public IP address) from key-value pair, using key 'ip'
        print(public_ip)
    except Exception as err:
        return f"Error: {err}"
print("\033[1mPublic IP Address:\033[0m")
get_public_ip()
print('')

# Display Default Gateway:

def get_default_gateway(): #function that gets Default Gateway IP addr, using netifaces module
    try:
        # Get default gateway for the default interface (usually 'eth0' or 'wlan0'):
        # Use netifaces.gateways() to get dictionary of gateway info...
        # Then filter for 'default', then filter for IPv4, and get the first result...
        # Which is the Default Gateway IP Address
        dg_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
        print(dg_ip)
    except (KeyError, netifaces.gaierror) as err:
        print(f"Error: {err}")
        return None
print("\033[1mDefault Gateway IP Address:\033[0m")
get_default_gateway()
print('')



#v. DISPLAY HARD DISK SIZE, FREE & USED SPACE

def get_disk_size(): #function that gets and prints hard disk size & space, using psutil module
    try:
        # Get disk usage statistics:
        disk_usage = psutil.disk_usage('/') #use psutil to get disk size & space info of directory '/'

        hd_size = disk_usage.total
        free_space = disk_usage.free
        used_space = disk_usage.used

        # Convert from bytes (default unit) to gigabytes:
        hd_size_gb = round(hd_size / (1024 ** 3), 3)
        free_space_gb = round(free_space / (1024 ** 3), 3)
        used_space_gb = round(used_space / (1024 ** 3), 3)
        
        print(f"- Hard Disk Size: {hd_size_gb} GB")
        print(f"- Hard Disk Free Space: {free_space_gb} GB")
        print(f"- Hard Disk Used Space: {used_space_gb} GB")

    except Exception as err:
        print(f"Error: {err}")

print("\033[1mHard Disk Details:\033[0m")
get_disk_size()
print('')



#vi. DISPLAY TOP 5 DIRECTORIES & THEIR SIZE

def top_directories(): #function that gets directory info, by running command in Terminal with subprocess module
    # Define the command to type in terminal:
    # Virtual and dynamic directories are excluded as they do not reflect true/persistent storage
    termcmd = "sudo du -b --exclude=/proc --exclude=/sys --exclude=/dev --exclude=/run / | sort -nr | head -n5"
    
    # Use 'subprocess.run()' to execute the command in terminal, and capture the output
    result = subprocess.run(termcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print the output or handle it as needed
    if result.returncode == 0:
        # Split the lines and extract size and directory
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if line:
                size, directory = re.split(r'\s+', line, maxsplit=1)
                print(f"Rank {i+1}: {directory.ljust(20)} {int(size)/10**9} GB")
    else:
        print(result.stderr)

print("\033[1mTop 5 Largest Directories & Sizes:\033[0m")
top_directories()
print('')



#vii. DISPLAY CPU USAGE (REFRESH EVERY 10s)

from datetime import datetime

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

print("\033[1mDisplay CPU Usage/Utilization Rate:\033[0m")
print("(refreshes every 10 seconds, press Control+C to exit...)")

while True:
    cpu_usage = get_cpu_usage()
    current_time = datetime.now().strftime("%d %b %Y %I:%M:%S %p")
    print(f"CPU Usage: {cpu_usage}% (Time now: {current_time})")
    time.sleep(10)
