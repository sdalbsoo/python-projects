# from pathlib import Path
import logging
import os


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        formatter1 = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")  # noqa
        formatter2 = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] - %(message)s")

        logger.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "INFO")))

        # log_file = os.environ.get("LOG_FILE")
        # if log_file is not None:
            # Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            # fileHandler = logging.FileHandler(log_file, mode="w")
            # fileHandler.setFormatter(formatter)
            # logger.addHandler(fileHandler)

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter2)
        logger.addHandler(streamHandler)

    return logger
