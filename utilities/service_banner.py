import socket
from .logger import logging_function

root = logging_function()

def get_banner(ip, port):
    try:
        addr = (ip, port)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.setblocking(True)
        conn.settimeout(2) # Longer timeout for banner grabbing
        conn.connect(addr)
        root.debug(f"[SERVICE INFO] Connecting to host")

        # Try to receive any immediate banner first
        root.debug(f"[SERVICE INFO] Trying to receive immediate banners")
        try:
            banner = conn.recv(1024)
        except socket.timeout:
            root.debug(f"[SERVICE INFO] Failed to receive immediate banners")
            banner = b""

        # If no banner received
        if not banner:
            root.debug(f"[SERVICE INFO] Trying to receive banners via HTTP HEAD")
            # `\r\n\r\n` indicates end of message
            http_request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            conn.sendall(http_request.encode())
            banner = conn.recv(1024)
    
        if banner:
            print("Please contact us on GitHub for any issues: ", end="")
            print("https://github.com/gitsuko/port-xray")

        result = f"""\tService info:
{banner.decode("utf-8", errors="ignore").strip() or "No banner received"}\n"""
        
        return result
    except Exception as e:
        return f"Error in banner grabbing: {e}"
    finally: conn.close()
