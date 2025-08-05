from datetime import datetime as dt, timedelta
from arguments import args
import logging as lo
import socket as so

# ================= LOGGER FOR STDOUT AND FILE =================
format = "%(asctime)s - %(levelname)s - %(message)s"
root = lo.getLogger()
root.setLevel(lo.INFO)

fileHandler = lo.FileHandler("logger.txt")
fileHandler.setFormatter(lo.Formatter(format, datefmt="%Y-%M-%d %H:%M:%S"))

consoleHandler = lo.StreamHandler()
consoleHandler.setFormatter(lo.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))

root.addHandler(fileHandler)
root.addHandler(consoleHandler)

# ================= CALCULATION FOR TIME DURATION =================
def format_timedelta(tdelta: timedelta) -> str:
    """
    Formats a datetime.timedelta object into a string with the format HH:MM:SS:MS.

    Parameters:
        tdelta (datetime.timedelta): The time duration to format.

    Returns:
        str: The formatted duration string in the format "HH:MM:SS:MS".
    """

    total_seconds = int(tdelta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    ms = int(tdelta.microseconds / 100)
    
    return f"{hours:02}:{minutes:02}:{seconds:02}:{ms:04}"

# ================= USER'S INPUT =================
def get_ip_addr(value):
    print(f"IP address to scan set to: {value}")
    return value

def get_port(value): 
    if "-" not in value: # for single port like 80
        if value.isdigit():
            print(f"Port set to: {value}")
            return int(value)
        else:
            return None
    
    else: # for a range of ports like 80-144
        parts = value.split("-")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            start_port, end_port = int(parts[0]), int(parts[1])
            print(f"Port set to: {start_port}-{end_port}")
            return (start_port, end_port)
        else:
            return None

data = args(get_port=get_port, get_host=get_ip_addr) # arguments function

while True:
    try:
        if not hasattr(data, "address") or data.address is None:
            address = input("Enter your IP address to scan: ")
            data.address = get_ip_addr(address)
        
        if not hasattr(data, "port") or data.port is None:
            port_input = input("enter port (e.g. 80 or 80-443): ")
            parsed = get_port(port_input)

            if parsed is None:
                raise ValueError("Invalid port format")
            data.port = parsed
        
        break # valid input, exit loop

    except (TypeError, ValueError):
        root.error("Port should be digits only.")

# ================= MAIN CODE =================
try: # for range scan
    start_port = int(data.port[0])
    end_port = int(data.port[1])
    mode = "range"
except: # for single scan
    port = data.port
    mode = "single"

time_start = dt.now()
root.info(f"Starting scan on {data.address} ...")

try:
    ADDRESS = data.address
    so.setdefaulttimeout(1) # Timeout for all sockets

    if mode == "range": # Range scan
        count = 0 # keep track of closed connections
        for port in range(start_port, end_port + 1):
            conn = so.socket(so.AF_INET, so.SOCK_STREAM)

            data = conn.connect_ex((ADDRESS, port))
            conn.close()

            if data == 0: # succeed code
                root.info(f"Connection on port {port} is open")
            else:
                count += 1
        
        root.info(f"closed port(s): {count}")

    else: # Single scan
        conn = so.socket(so.AF_INET, so.SOCK_STREAM)

        data = conn.connect_ex((ADDRESS, port))
        conn.close()

        if data == 0: # succeed code
            root.info(f"Connection on port {port} is open")
        else:
            root.info(f"Connection on port {port} is closed")

except Exception as e:
    root.error(f"{e}")

# calculating time duration
time_end = dt.now()
time_duration = time_end - time_start
root.info(f"scan took {format_timedelta(time_duration)}")