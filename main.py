from utilities.time_duration import format_timedelta
from utilities.logger import logging_function
from datetime import datetime as dt
from arguments import args
import socket as so
import sys

# ================= WELCOME MESSAGE =================
print("############################################################")
print("DISCLAIMER: THIS SCRIPT IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.")
print("AUTHOR TAKES NO RESPONSIBILITY FOR USER'S USAGE.")
print("############################################################")

# ================= LOGGER =================
root = logging_function()

# ================= USER'S INPUT =================
def get_ip_subnet(ip_addr: str):
    """
    Expands a subnet into a list of addresses

    Parameters:
        ip_addr (str): The IP address subnet (e.g. 192.168.1.1/24)
    
    Returns:
        list (str): A list of IP addresses included in the given subnet
    """
    global subnet_class
    try:
        address = ip_addr.split("/")[0]
        subnet_class = ip_addr.split("/")[1]
        
        if subnet_class == "32":
            return address
        elif subnet_class == "24":
            seperate_addr = address.rsplit(".", 1)
            static_ip = seperate_addr[0] # e.g. 192.168.1.X
            
            result = list()
            for i in range(1, 255):
                result.append(f"{static_ip}.{i}")

            return tuple(result)
        elif subnet_class == "16":
            root.error("Refusing to scan public or unsafe IP ranges. Exiting for safety.")
            sys.exit()

        elif subnet_class == "8":
            root.error("Refusing to scan public or unsafe IP ranges. Exiting for safety.")
            sys.exit()

        elif subnet_class == "0":
            root.error("Refusing to scan the entire internet. Exiting for safety.")
            sys.exit()

        else:
            pass

    except Exception as e:
        root.error(f"error in get_ip_subnet: {e}")

subnet = False # Defalut value

def get_ip_addr(value):
    global subnet
    if "/" in value: # for range of IP addresses
        subnet = True
        return get_ip_subnet(value)
    else: # for single IP address
        subnet = False
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
count = 0 # keep track of closed connections

try:
    so.setdefaulttimeout(0.5) # Timeout for all sockets
    ADDRESS = data.address

    if mode == "range": # Range scan

        if type(ADDRESS) == tuple: # range Ip scan
            for i in range(len(ADDRESS)):
                addr = str(ADDRESS[i])
                
                for port in range(start_port, end_port + 1):
                    conn = so.socket(so.AF_INET, so.SOCK_STREAM)

                    data = conn.connect_ex((addr, port))
                    conn.close()

                    if data == 0: # succeed code
                        root.info(f"Connection on {addr}:{port} is open")
                    else:
                        count += 1
            
            root.info(f"closed port(s): {count}")
        
        else: # range port for single IP address
            root.info(f"Starting scan on {ADDRESS}")
            for port in range(start_port, end_port + 1):
                    conn = so.socket(so.AF_INET, so.SOCK_STREAM)

                    data = conn.connect_ex((ADDRESS, port))
                    conn.close()

                    if data == 0: # succeed code
                        root.info(f"Connection on {ADDRESS}:{port} is open")
                    else:
                        count += 1
            
            root.info(f"closed port(s): {count}")

    else: # Single port scan

        if type(ADDRESS) == tuple: # for range of ip address
            for i in range(len(ADDRESS)):
                addr = str(ADDRESS[i])

                conn = so.socket(so.AF_INET, so.SOCK_STREAM)

                data = conn.connect_ex((addr, port))
                conn.close()

                if data == 0: # succeed code
                    root.info(f"Connection on {addr}:{port} is open")
                else:
                    count += 1

            root.info(f"closed port(s): {count}")

        else: #for single ip
            root.info(f"Starting scan on {ADDRESS}")
            conn = so.socket(so.AF_INET, so.SOCK_STREAM)

            data = conn.connect_ex((ADDRESS, port))
            conn.close()

            if data == 0: # succeed code
                root.info(f"Connection on port {port} is open")
            else:
                root.info(f"Connection on port {port} is closed")

except KeyboardInterrupt:
    root.error("Ctrl+C pressed. exiting...")
    sys.exit()

except Exception as e:
    root.error(f"error in main code: {e}")

# calculating time duration
time_end = dt.now()
time_duration = time_end - time_start
root.info(f"scan took {format_timedelta(time_duration)}")