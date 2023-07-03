#!/usr/bin/env python3
#A simple script to spot-check Phusion Passenger when the settings in config fail.
#Run with a cronjob and touch a file in tmp or something to create a log of actions.
#Revamped with memory and proccesed request count checking, made more modular. 
import subprocess
import re
import os
import time
import datetime

# Set the thresholds for the script
timeout_seconds = 330
memory_limit = 3072
processed_limit = 10000

# Parse the output of passenger-status to xml
output = subprocess.check_output(['passenger-status', '--show=xml'])
output = output.decode('utf-8')

# Timeout Checking
pids_and_last_used = re.findall(r'<pid>(\d+)</pid>.*?<last_used>(\d+)</last_used>', output, re.DOTALL)
print("PIDs and last_used:", pids_and_last_used)

for pid, last_used in pids_and_last_used:
    pid = int(pid)
    last_used = int(last_used)
    current_time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    print("Checking PID %d with last_used %d" % (pid, last_used))

    time_difference = (time.time() * 1000000 - last_used) / 1000000
    print("Time difference (seconds):", time_difference)
    print("Timeout (seconds):", timeout_seconds)

    if time_difference > timeout_seconds:
        print('%s Killing process with PID %d due to inactivity' % (current_time, pid))
        os.system('kill -s USR1 %d' % pid)
    else:
        print('%s Process with PID %d is still active' % (current_time, pid))

# Memory Checking
pids_and_memory = re.findall(r'<pid>(\d+)</pid>.*?<real_memory>(\d+)</real_memory>', output, re.DOTALL)
print("PIDs and Memory:", pids_and_memory)

for pid, memory in pids_and_memory:
    pid = int(pid)
    memory = int(memory.rstrip('M')) / 1024
    current_time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    print("Checking PID %d with memory %dM" % (pid, memory))
    print("Memory Limit(MB):",memory_limit)
    if memory >= memory_limit:
        print('%s Killing process with PID %d due to high memory usage' % (current_time, pid))
        os.system('kill -s USR1 %d' % pid)
    else:
        print('%s Process with PID %d is within memory limit' % (current_time, pid))

# Requests processed
pids_and_processed = re.findall(r'<pid>(\d+)</pid>.*?<processed>(\d+)</processed>', output, re.DOTALL)
print("PIDs and Processed:", pids_and_processed)

for pid, processed in pids_and_processed:
    pid = int(pid)
    processed = int(processed)
    current_time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    print("Checking PID %d with processed %d" % (pid, processed))
    print("Processed Limit:", processed_limit)
    if processed >= processed_limit:
        print('%s Killing process with PID %d due to high request count' % (current_time, pid))
        os.system('kill -s USR1 %d' % pid)
    else:
        print('%s Process with PID %d is within request limit' % (current_time, pid))

