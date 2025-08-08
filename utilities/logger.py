import logging as lo

def logging_function():
    file_format = "%(asctime)s - %(levelname)s - %(message)s"
    stdout_format = "%(asctime)s - %(message)s"
    root = lo.getLogger()
    root.setLevel(lo.INFO)

    fileHandler = lo.FileHandler("logger.txt")
    fileHandler.setFormatter(lo.Formatter(file_format, datefmt="%Y-%M-%d %H:%M:%S"))

    consoleHandler = lo.StreamHandler()
    consoleHandler.setFormatter(lo.Formatter(stdout_format, datefmt="%H:%M:%S"))

    root.addHandler(fileHandler)
    root.addHandler(consoleHandler)

    return root