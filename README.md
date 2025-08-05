# port-xray

A simple command-line port scanner written in Python.

## Features

- Uses Python built-in modules
- Supports TCP scanning
- CLI argument support with fallback to interactive mode

## Usage

Run the scanner interactively:

```bash
python3 main.py
```
Or pass command-line arguments:

```bash
python3 main.py -a 127.0.0.1 -p 80
```
Use -h or --help to display available options.

## Arguments
`-a ADDRESS`, `--address ADDRESS`

Target IP address to scan.

`-p PORT`, `--port PORT`

Port(s) to scan. Supports a single port (80) or a range (20-100).

## Planned Features

- Add support for UDP scanning

- Parallel (multi-threaded) scanning for speed
