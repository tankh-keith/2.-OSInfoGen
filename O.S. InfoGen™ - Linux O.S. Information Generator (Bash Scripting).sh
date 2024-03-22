#!/bin/bash

#i. Introductory Statement
echo
echo -e "\e[1mWelcome to Keith Tan's Linux O.S. Information Generator.\e[0m \nHere are your machine's O.S. Details:"
echo

#1. Display the Linux Version:
: <<'References for #1'
- ChatGPT 3.5
References for #1
echo -e "\e[1mLinux Version Details:\e[0m"
linux_ver=$(cat /etc/os-release | head -n5 | grep -v PRETTY)
echo "$linux_ver"
echo

#2. Display the Private IP Address, Public IP Address, Default Gateway:
: <<'References for #2'
- Hackersploit: Shell Scripting - If & If/else: https://www.youtube.com/watch?v=qoem5hqCH6A
- Learn Linux TV: Bash Scripting on Linux (The Complete Guide): https://www.youtube.com/watch?v=2733cRPudvI
References for #2
echo -e "\e[1mIP Address Details:\e[0m"

#Private IP Address
private_IP=$(ifconfig | grep broadcast | awk '{print $2}')
echo "The Private IP Address is: $private_IP"

#Public IP Address:
urls=("ifconfig.whoops" "ifconfig.io" "ifconfig.co" "ifconfig.me")
public_IP=""

for url in "${urls[@]}"; 
	do 
	public_IP=$(curl -s "$url")
    #input-validation:
    if [ -n "$public_IP" ]; then
        echo "The Public IP Address is: $public_IP"
        break  #once Public IP is obtained, quit looping.
    else
    #error-handling:
        echo "Failed to retrieve the Public IP Address from $url. Trying the next one..."
    fi
done

#Default Gateway:
def_gateway=$(route | grep default | awk '{print $2}')
echo "The Default Gateway is: $def_gateway"
echo


#3 Display the Hard Disk Size; Free & Used Space:
:<<'References for #3' 
- Linux Theatre: Disk Partitioning in Linux: https://www.youtube.com/watch?v=cP1TqdOJNj8
- Linux Foundation: https://www.linuxfoundation.org/blog/blog/classic-sysadmin-how-to-check-disk-space-on-linux-from-the-command-line
- ChatGPT 3.5
References for #3
if lscpu | grep -q "Intel"; then
    diskname="sda1" # Windows host running Linux O.S.
elif (lscpu | grep -q "Apple") || [ -d "/Volumes/Macintosh HD" ]; then
    diskname="nvme0n1p2" # macOS host running Linux O.S.
else
    diskname="nvme0n1p2" # Native Linux host or unknown
fi

harddisk_sizeGB=$(lsblk -b | grep "$diskname" | awk '{print $4 / 10**9}')"GB"
harddisk_sizeMB=$(lsblk -b | grep "$diskname" | awk '{print $4 / 10**6}')"MB"
harddisk_free=$(df -h | grep "$diskname" | awk '{print $4}')"B"
harddisk_used=$(df -h | grep "$diskname" | awk '{print $3}')"B"
echo -e "\e[1mHard Disk Details:\e[0m"
echo "The Hard Disk Size is: $harddisk_sizeGB ($harddisk_sizeMB)"
echo "The Hard Disk Free (available) Space is: $harddisk_free"
echo "The Hard Disk Used Space is: $harddisk_used"
echo


#4. Display the Top 5 Directories and their Size:
:<<'References for #4'
- Linux Foundation: https://www.linuxfoundation.org/blog/blog/classic-sysadmin-how-to-check-disk-space-on-linux-from-the-command-line
- Learn Linux TV: Bash Scripting on Linux (The Complete Guide): https://www.youtube.com/watch?v=2733cRPudvI
- Linuxhint: Bash Loops {For, Until and While Loops}: https://www.youtube.com/watch?v=_zdChpzuWrU
References for #4
echo -e "\e[1mTop 5 Directories (and Sizes):\e[0m"
top5_dir_info=$(sudo du -b --exclude={/proc,/sys,/dev,/run} / | sort -nr | head -n5)
i=1
echo "$top5_dir_info" | while read size path
do
  echo "Rank $i: $path (Size = $((size / 10**9))GB)"
  ((i++))
done
echo


#5. Display the CPU usage; Refresh every 10 seconds:
:<<'References for #5' 
- StackOverflow: https://stackoverflow.com/questions/62357115/bash-how-to-make-a-script-that-update-every-x-seconds-and-it-repeats-forever
- Site24x7: CPU Utilization: https://www.site24x7.com/learn/linux/cpu-utilization.html
References for #5
echo -e "\e[1mCPU Usage/Utilization Rates:\e[0m \n(loads every 10s, press Control+C to Exit!)"
while true;
do
curr_time=$(date +"%d/%m/%y %H:%M:%S")
CPU_uti_rate=$(mpstat 1 1 | tail -n1 | awk '{uti = 100 - $NF} END {print uti}')"%"
echo "The CPU Usage/Utilization Rate is currently at $CPU_uti_rate  (Time now: $curr_time)"
sleep 10
done 
