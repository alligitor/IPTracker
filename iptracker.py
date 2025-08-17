from datetime import datetime
import time
import subprocess
import sys


hosts = [
"192.168.68.1", #router
"192.168.68.10",
"192.168.68.12",
"8.8.8.8", #google's DNS
"1.1.1.1" #cloud flare's DNS
]

hostArray = {host: 1 for host in hosts}

printHostIsDead = False
printHostIsAlive = False
printHostHadOutage = False

#parse the command line arguments
for arg in sys.argv[1:]:
    if arg == "-d":
        printHostIsDead = True
    elif arg == "-a":
        printHostIsAlive = True
    elif arg == "-o":
        printHostHadOutage = True
    elif arg == "-h":
        print(f"Usage: {sys.argv[0]} [-d] [-a] [-o]")
        print("    -d prints a message every time a host misses a ping")
        print("    -a prints a message every time a host responds to a ping")
        print("    -o prints length of the outage every time a host comes back to life")
        sys.exit(1)

timeStampPrintDelay = 0

while True:
    result = subprocess.run(["/usr/bin/fping", '-r', '0'] + hosts, capture_output=True, text=True)
    output = result.stdout.splitlines()

    date = datetime.now().strftime('%Y%m%d-%H%M%S')

    if timeStampPrintDelay == 0:
        print(f"---------------[{date}]-----------------")
        timeStampPrintDelay = 10
    else:
        timeStampPrintDelay = timeStampPrintDelay - 1

    for line in output:
        host = line.split()[0]

        if "live" in line:
            if hostArray[host] != 0:
                if printHostHadOutage:
                    print(f"{date}, host {host} had an outage of {hostArray[host]} ticks")

            if printHostIsAlive:
                print(f"{date}, {host} is ALIVE")

            hostArray[host] = 0
        else:
            hostArray[host] += 1
            if printHostIsDead:
                print(f"{date}, {host} is DEAD - {hostArray[host]} ticks")
            if (hostArray[host] % 10) == 0:
                print(f"{date}, {host} is still DEAD after {hostArray[host]} ticks")

    time.sleep(1)

