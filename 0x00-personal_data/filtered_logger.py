#!/usr/bin/env python3
"""
filtered_datum module - Contains the filter_datum function
"""

import re
from typing import List

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

