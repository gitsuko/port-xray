from utilities.time_duration import format_timedelta
from utilities.logger import logging_function
from datetime import datetime as dt
from arguments import args
import logging as lo
import socket as so
import sys


# ================= LOGGER =================
root = logging_function()

# ================= IP RANGE HANDLING FUNCTIONS =================
def get_ip_subnet(ip_addr: str):
    """
    Expands a subnet into a list of IP addresses.

    Parameters:
        ip_addr (str): The subnet in CIDR notation (e.g., "192.168.1.0/24").

    Returns:
        tuple:
            - A tuple of IP addresses if the expansion is successful.

        #### str
            - A string of single IP address for /32 subnet.
    """
    global subnet_class
    try:
        address = ip_addr.split("/")[0]
        subnet_class = ip_addr.split("/")[1]
        
        if subnet_class == "32":
            return address
        elif subnet_class == "24":
            seperate_addr = address.rsplit(".", 1)
            static_ip = seperate_addr[0]
            
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

def get_ip_range(ip_addr):
    """
    Expands a IP range into a list of IP addresses.

    Parameters:
        ip_addr (str): IP address (e.g., "192.168.10.15-30").

    Returns:
        tuple:
            - A tuple of IP addresses if the expansion is successful.

        #### str
            - A string of a single IP address.
    """
    fragments = ip_addr.split(".")
    
    if len(fragments) < 4: # error handling (e.g. 192.168.10-15)
        root.error("IP address is wrong.")
        return None
    
    range_value = fragments[-1]
    static_ip = ".".join(fragments[:-1])
    
    if "-" in static_ip:
        root.error("IP range scan supports last digit only")
        print("Right format: 192.168.1.1-10")
        print("Wrong formats: 192.168.1-10.1 , 192.168-188.1.1")
        return None

    start_range, end_range = range_value.split("-")
    
    result = list()
    for i in range(int(start_range), int(end_range) + 1):
        result.append(f"{static_ip}.{i}")
    
    return tuple(result)

# ================= USER'S INPUT =================
subnet = False # Defalut value

def get_ip_addr(value):
    global subnet
    if "/" in value: # for IP address with subnet mask
        subnet = True
        return get_ip_subnet(value)
    elif "-" in value: # for range IP address
        return get_ip_range(value)
    else: # for single IP address
        subnet = False
        print(f"Host to scan set to: {value}")
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

def get_timeout(time=0.5):
    try:
        if time:
            return int(time)
        else:
            return 0.5
    except (TypeError, ValueError):
        root.info("time out value must be digit")
        sys.exit(1)

data = args(get_host=get_ip_addr, get_port=get_port, get_timeout=get_timeout) # arguments function

# check verbosity
if data.verbose:
    root.setLevel(lo.DEBUG)

# check for legal message
if data.legal:
    print("############################################################")
    print("DISCLAIMER: THIS SCRIPT IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.")
    print("AUTHOR TAKES NO RESPONSIBILITY FOR USER'S USAGE.")
    print("############################################################")
    print()

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
    
    except KeyboardInterrupt:
        print()
        root.error("Ctrl+C pressed. exiting...")
        sys.exit()
# ================= MAIN CODE =================

try: # for range scan
    start_port = int(data.port[0])
    end_port = int(data.port[1])
    mode = "range"
except: # for single scan
    port = data.port
    mode = "single"

root.debug("[TIME] Starting time for calculating duration")
time_start = dt.now()
count = 0 # keep track of closed connections

try:
    time_out = data.time_out
    if time_out is None:
        time_out = 0.5
    so.setdefaulttimeout(time_out) # Timeout for all sockets
    root.debug(f"[SOCKET TIMEOUT] Set socket timeout to {time_out}s")
    ADDRESS = data.address

    if mode == "range": # Range scan
        if type(ADDRESS) == tuple: # range Ip scan
            root.debug("[TAGET] Preparing IP ranges for scan")
            for i in range(len(ADDRESS)):
                addr = str(ADDRESS[i])
                
                for port in range(start_port, end_port + 1):
                    conn = so.socket(so.AF_INET, so.SOCK_STREAM)

                    data = conn.connect_ex((addr, port))
                    conn.close()

                    if data == 0: # succeed code
                        if not root.debug(f"Connection on {addr}:{port} is open"):
                            root.info(f"Connection on {addr}:{port} is open") 
                    else:
                        root.debug(f"Connection on {addr}:{port} is close")
                        count += 1
            
            root.info(f"closed port(s): {count}")
            root.info(f"Total host scanned: {len(ADDRESS)}")
        
        else: # range port for single IP address
            root.info(f"Starting scan on {ADDRESS}")
            for port in range(start_port, end_port + 1):
                    conn = so.socket(so.AF_INET, so.SOCK_STREAM)

                    data = conn.connect_ex((ADDRESS, port))
                    conn.close()

                    if data == 0: # succeed code
                        root.info(f"Connection on {ADDRESS}:{port} is open")
                    else:
                        root.debug(f"Connection on {ADDRESS}:{port} is closed")
                        count += 1
            
            root.info(f"closed port(s): {count}")

    else: # Single port scan

        if type(ADDRESS) == tuple: # for range of ip address
            root.debug("[TAGET] Preparing IP ranges for scan")
            for i in range(len(ADDRESS)):
                addr = str(ADDRESS[i])

                conn = so.socket(so.AF_INET, so.SOCK_STREAM)

                data = conn.connect_ex((addr, port))
                conn.close()

                if data == 0: # succeed code
                    root.info(f"Connection on {addr}:{port} is open")
                else:
                    root.debug(f"Connection on {addr}:{port} is closed")
                    count += 1

            root.info(f"closed port(s): {count}")
            root.info(f"Total host scanned: {len(ADDRESS)}")

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
    conn.close()
    sys.exit()

except Exception as e:
    root.error(f"error in main code: {e}")

# calculating time duration
root.debug("[TIME] Stopping time for calculating duration")
time_end = dt.now()
time_duration = time_end - time_start
root.info(f"scan took {format_timedelta(time_duration)}")