import logging
import os


def get_logger(name, log_file=None):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")

        logger.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "INFO")))

        if log_file is not None:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fileHandler = logging.FileHandler(log_file, mode="w")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

    return logger
