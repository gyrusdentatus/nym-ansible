import socket
import requests
import time

local_ip = "127.0.0.1"
rpc_port = 26657
statsd_port = 8125
# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
rpc = ('http://mixnet.club/status') 
resp = requests.get(rpc)
height = (resp.json().get('result').get('sync_info').get('latest_block_height'))
while True:
    rpc = ('http://mixnet.club/status')  
    resp = requests.get(rpc)
    height = (resp.json().get('result').get('sync_info').get('latest_block_height'))
    print(height,"is now the latest height")
    t = ("figment_ops_challenge.gyrusdentatus:", height,"|g")
    gauge = ''.join(t) 
    while int(height) != int(height) + 1:
        s.sendto(gauge.encode('ascii'), (local_ip, statsd_port))
        print(height)
        time.sleep(6)
        break
 
    time.sleep(4)
    # close the socket
    s.close()