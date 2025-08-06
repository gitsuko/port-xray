import argparse

def args(get_host, get_port):
    description = """
    This is simple Port Scanner app written in python.
    Currect protocol supprting: TCP.
    
    Examples:
        python3 main.py -a 192.168.10.10 -p 80-120
        python3 main.py -a 192.168.10.10/24 -p 80
        python3 main.py -a 192.168.10.10-20 -p 80"""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument(
        "-a", "--address",
        type=get_host,
        help="IP address to scan."
    )

    parser.add_argument(
        "-p", "--port",
        type=get_port,
        help="Port(s) for scanning target. It should be digits only. (e.g. -p 443 or -p 80-443)"
    )

    return parser.parse_args()
