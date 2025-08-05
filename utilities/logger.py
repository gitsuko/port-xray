import logging as lo

def logging_function():
    format = "%(asctime)s - %(levelname)s - %(message)s"
    root = lo.getLogger()
    root.setLevel(lo.INFO)

    fileHandler = lo.FileHandler("logger.txt")
    fileHandler.setFormatter(lo.Formatter(format, datefmt="%Y-%M-%d %H:%M:%S"))

    consoleHandler = lo.StreamHandler()
    consoleHandler.setFormatter(lo.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))

    root.addHandler(fileHandler)
    root.addHandler(consoleHandler)

    return root