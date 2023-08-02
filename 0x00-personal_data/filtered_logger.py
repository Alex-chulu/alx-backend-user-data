#!/usr/bin/env python3
"""
filtered_logger module - Contains the RedactingFormatter class and filter_datum function
"""

import logging
import re
from typing import List

class RedactingFormatter(logging.Formatter):
    """
    RedactingFormatter class - Custom log formatter that obfuscates specified fields
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter object.

        Args:
            fields (List[str]): List of strings representing all fields to obfuscate.

        Returns:
            None
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log message and obfuscate specified fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with obfuscated fields.
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

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

