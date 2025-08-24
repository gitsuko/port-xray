import logging

def logging_function():
    file_format = "%(asctime)s - %(levelname)s - %(message)s"
    stdout_format = "%(message)s"
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if not root.handlers: # To avoid multiple logging
        fileHandler = logging.FileHandler("logger.txt")
        fileHandler.setFormatter(logging.Formatter(file_format, datefmt="%Y-%M-%d %H:%M:%S"))

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter(stdout_format, datefmt="%H:%M:%S"))

        root.addHandler(fileHandler)
        root.addHandler(consoleHandler)

    return root