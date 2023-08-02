#!/usr/bin/env python3
"""
Filtered Logger module
"""

import logging
import re
from typing import List
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "********"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize the RedactingFormatter object.

        Args:
            fields (List[str]): List of fields to obfuscate in the log message.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Filter and obfuscate certain fields in the log message.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): The string used for obfuscation.
        message (str): The log message.
        separator (str): The character separating all fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        pattern = r"(?<={}=)(.*?)(?={})".format(field, separator)
        message = re.sub(pattern, redaction, message)
    return message


def get_logger() -> logging.Logger:
    """ Return a logging.Logger object named "user_data".

    The logger should log up to logging.INFO level, should not propagate messages to other loggers,
    and should have a StreamHandler with RedactingFormatter as the formatter.

    Returns:
        logging.Logger: The "user_data" logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a connector to the secure Holberton database.

    The database credentials are obtained from environment variables
    PERSONAL_DATA_DB_USERNAME, PERSONAL_DATA_DB_PASSWORD, PERSONAL_DATA_DB_HOST, and PERSONAL_DATA_DB_NAME.

    Returns:
        mysql.connector.connection.MySQLConnection: The connector to the database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def main():
    """ Main function to retrieve all rows from the users table and display each row in a filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    for row in cursor.fetchall():
        log_record = "; ".join([f"{field}={value}" for field, value in zip(PII_FIELDS, row)])
        logger = get_logger()
        logger.info(log_record)


if __name__ == "__main__":
    main()

