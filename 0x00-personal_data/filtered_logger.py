#!/usr/bin/env python3
"""
filtered_logger module - Contains functions related to logging user data with obfuscation
"""

import logging
import csv
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "********"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s - %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(PII_FIELDS, self.REDACTION, super().format(record), self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate the specified fields in the log message.

    Args:
        fields (List[str]): List of strings representing all fields to obfuscate.
        redaction (str): The string representing by what the field will be obfuscated.
        message (str): The log line to be obfuscated.
        separator (str): The string representing by which character is separating all fields in the log line.

    Returns:
        str: The log message with obfuscated fields.
    """
    return re.sub(rf"({'|'.join(fields)})=.*?{separator}", f"\\1={redaction}{separator}", message)

def get_logger() -> logging.Logger:
    """
    Returns a logger named "user_data" that logs up to logging.INFO level.
    It does not propagate messages to other loggers and has a StreamHandler with RedactingFormatter as formatter.

    Returns:
        logging.Logger: The logger object for logging user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


