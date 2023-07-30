from flask import Flask, jsonify, make_response
import socket
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, this is the main endpoint!"

def http_health_check(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def tcp_health_check(host, port):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except (socket.timeout, ConnectionError):
        return False

@app.route('/health/http')
def health_check_1():
    # Implement your first health check logic here (HTTP-based check)
    folder_path = "/app/health1"  # Replace with the path to your folder containing the health check file
    
    health_check_file = os.path.join(folder_path, "http_health_check.txt")
    if os.path.exists(health_check_file):
        with open(health_check_file, "r") as file:
            url = file.read().strip()
            if url:
                if http_health_check(url):
                    return jsonify({"status": "Health Check 1: OK"}), 200
    return jsonify({"status": "Health Check 1: Failed"}), 500

@app.route('/health/tcp')
def health_check_2():
    # Implement your second health check logic here (TCP-based check)
    folder_path = "/app/health2"  # Replace with the path to your folder containing the health check file
    
    health_check_file = os.path.join(folder_path, "tcp_health_check.txt")
    if os.path.exists(health_check_file):
        with open(health_check_file, "r") as file:
            data = file.read().strip()
            if data:
                host, port = data.split(":")
                if tcp_health_check(host, int(port)):
                    return jsonify({"status": "Health Check 2: OK"}), 200
    return jsonify({"status": "Health Check 2: Failed"}), 500

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

