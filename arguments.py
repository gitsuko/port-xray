import argparse

def args(get_host, get_port):
    description = """
    This is simple Port Scanner app written in python.
    Currect protocol supprting: TCP."""

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
