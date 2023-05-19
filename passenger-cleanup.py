#!/usr/bin/env python3
#A simple script to spot-check Phusion Passenger when the settings in config fail.
#Run with a cronjob and touch a file in tmp or something to create a log of actions.
import subprocess
import re
import os
import time
import datetime

output = subprocess.check_output(['passenger-status', '--show=xml'])
output = output.decode('utf-8')
pids_and_last_used = re.findall(r'<pid>(\d+)</pid>.*?<last_used>(\d+)</last_used>', output, re.DOTALL)

print("PIDs and last_used:", pids_and_last_used)

timeout_seconds = 360

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
