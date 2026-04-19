import socket
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

open_ports = []
lock = Lock()


def create_log_file():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"logs/scan_{timestamp}.txt"
    return file_path


log_file = create_log_file()



def log_result(message):
    with lock:
        with open(log_file, "a") as f:
            f.write(message + "\n")



def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((ip, port))

        if result == 0:
            msg = f"[OPEN] Port {port}"
            print(msg)

            with lock:
                open_ports.append(port)

            log_result(msg)

        sock.close()

    except:
        pass



def start_scan(ip, start_port, end_port):
    print(f"\nScanning {ip}...\n")
    log_result(f"Scanning {ip} from {start_port} to {end_port}")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port)

    if len(open_ports) == 0:
        print("\nNo open ports found.")
        log_result("No open ports found.")
    else:
        print(f"\nOpen ports: {open_ports}")
        log_result(f"Open ports: {open_ports}")



target = input("Enter IP: ")
start = int(input("Start port: "))
end = int(input("End port: "))

start_scan(target, start, end)