import logging

_logger = None


def init_logger(filename = None):
    global _logger
    _logger = logging.getLogger("twitch")
    _logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)

    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)


def log(*args):
    global _logger
    _logger.info(" ".join(str(arg) for arg in args))
