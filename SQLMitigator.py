import socket
import sqlite3
import threading
import re

server_ip = "0.0.0.0"
server_port = 9999

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'password'))
    conn.commit()
    conn.close()

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    print(f"Received: {request}")
    
    params = request.split('&')
    username = params[0].split('=')[1]
    password = params[1].split('=')[1]

    if not is_safe(username) or not is_safe(password):
        client_socket.send(b"Invalid input detected")
    else:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = 'SELECT * FROM users WHERE username=? AND password=?'
        c.execute(query, (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            client_socket.send(b"Login successful")
        else:
            client_socket.send(b"Invalid credentials")
    
    client_socket.close()

def is_safe(input_string):
    # Basic SQL Injection prevention using regex to check for common injection patterns
    pattern = re.compile(r"[;'\"]|(--)+")
    return not pattern.search(input_string)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    init_db()
    start_server()
