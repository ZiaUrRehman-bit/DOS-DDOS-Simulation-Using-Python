import socket
import threading
from collections import defaultdict
import time

server_ip = "0.0.0.0"
server_port = 8080
threshold = 100  # Number of requests before blocking
monitoring_window = 10  # Time window in seconds

request_count = defaultdict(int)
blocked_ips = set()
lock = threading.Lock()

def monitor_requests():
    while True:
        time.sleep(monitoring_window)
        with lock:
            for ip, count in list(request_count.items()):
                if count > threshold:
                    blocked_ips.add(ip)
                    print(f"Blocked IP: {ip} with {count} requests")
                request_count[ip] = 0  # Reset count after each window

def handle_client(client_socket, client_address):
    with lock:
        if client_address[0] in blocked_ips:
            client_socket.close()
            return

        request_count[client_address[0]] += 1
        if request_count[client_address[0]] > threshold:
            blocked_ips.add(client_address[0])
            print(f"Blocked IP: {client_address[0]}")

    client_socket.recv(1024)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def unblock_ip(ip):
    with lock:
        if ip in blocked_ips:
            blocked_ips.remove(ip)
            print(f"Unblocked IP: {ip}")

def cli():
    while True:
        command = input("Enter command (unblock <IP> or exit): ")
        if command.startswith("unblock"):
            _, ip = command.split()
            unblock_ip(ip)
        elif command == "exit":
            break

if __name__ == "__main__":
    monitoring_thread = threading.Thread(target=monitor_requests)
    monitoring_thread.start()

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    cli()
