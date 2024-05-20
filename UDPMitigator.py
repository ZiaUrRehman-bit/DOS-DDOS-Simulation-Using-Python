import socket
import threading
from collections import defaultdict
import time

server_ip = "0.0.0.0"
server_port = 9999
threshold = 100  # Number of UDP packets before blocking
monitoring_window = 10  # Time window in seconds

udp_count = defaultdict(int)
blocked_ips = set()
lock = threading.Lock()

def monitor_requests():
    while True:
        time.sleep(monitoring_window)
        with lock:
            for ip, count in list(udp_count.items()):
                if count > threshold:
                    blocked_ips.add(ip)
                    print(f"Blocked IP: {ip} with {count} UDP packets")
                udp_count[ip] = 0  # Reset count after each window

def handle_udp(server_socket):
    while True:
        data, client_address = server_socket.recvfrom(1024)
        with lock:
            if client_address[0] in blocked_ips:
                continue
            
            udp_count[client_address[0]] += 1
            if udp_count[client_address[0]] > threshold:
                blocked_ips.add(client_address[0])
                print(f"Blocked IP: {client_address[0]}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_ip, server_port))
    print(f"Listening on {server_ip}:{server_port}")

    handle_udp(server)

if __name__ == "__main__":
    monitoring_thread = threading.Thread(target=monitor_requests)
    monitoring_thread.start()

    start_server()
