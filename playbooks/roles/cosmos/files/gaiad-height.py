#!/usr/bin/python3

import socket
import requests
import time

local_ip = "127.0.0.1"
rpc_port = 26657
statsd_port = 8125
# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

while True:
    rpc = ('http://127.0.0.1:26657/status')
    # get the json from the rpc endpoint
    resp = requests.get(rpc)
    # parse the json to get only the latest_block_height 
    height = (resp.json().get('result').get('sync_info').get('latest_block_height'))
    # print the height for systemd service
    print("Gaiad-log: Latest height is now:", height)
    # new var for joining all the strings together so they could be sent to StatsD in the correct format
    t = ("figment_ops_challenge.gyrusdentatus:", height,"|g")
    gauge = ''.join(t)

    ## Send the results as a gauge to the StatsD server
    ## using while loop here in case the block time 
    ## was faster than 6 seconds. 
    ## Maybe using IF would be better, but I could not decide. 
    while int(height) != int(height) + 1:
        s.sendto(gauge.encode('ascii'), (local_ip, statsd_port))
        #print(height)
        time.sleep(6)
        break
    
    # sleep 4 seconds - 6 + 4 = 10 
    # as per challenge instructions
    time.sleep(4)