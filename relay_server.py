import serial
import socket
import threading

COM_PORT = "COM5"
BAUD = 9600
HOST = '127.0.0.1'  # localhost
PORT = 65432        # Arbitrary unused port

# Connect to HC-05 via serial
ser = serial.Serial(COM_PORT, BAUD)
print(f"[Relay] Connected to {COM_PORT}")

def handle_client(conn, addr):
    print(f"[Relay] New client connected from {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            ser.write(data)
            print(f"[Relay] Forwarded: {data.decode().strip()}")
    except Exception as e:
        print(f"[Relay] Client error: {e}")
    finally:
        conn.close()
        print(f"[Relay] Client from {addr} disconnected.")

# TCP Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Relay] Listening for clients on {HOST}:{PORT}...")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except :#KeyboardInterrupt:
        print("\n[Relay] Shutting down...")
    finally:
        ser.close()
        print("[Relay] COM port released.")
