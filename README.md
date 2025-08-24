# port-xray

A Python-based port scanner tool that supports service version grabbing.

## Features

- Supports TCP scanning
- Supports service version grabbing
- Supports single and range IP scan
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

## Arguments
![Arguments.png](./img/arguments.png)


## Planned Features

- Add support for UDP scanning

- Parallel (multi-threaded) scanning for speed

## Contribution

Contributions are welcome. Feel free to open an issue or a pull request.

## DISCLAIMER

This script is for educational and research purposes only.
Use at your own risk — the author takes no responsibility.
