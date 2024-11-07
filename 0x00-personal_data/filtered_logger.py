#!/usr/bin/env python3
"""Write a function called filter_datum"""
import re
from typing import List
import logging


PII_FIELDS = ('phone', 'ssn', 'password', 'ip', 'last_login')


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    for fld in fields:
        message = re.sub(
                rf'{fld}=[^{separator}]*', f"{fld}={redaction}", message)
    return message


def get_logger() -> logging.Logger:
    """ takes no arguments and returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(hdlr)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init Method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns log format string"""
        record.msg = filter_datum(
                self.fields,
                self.REDACTION,
                record.getMessage(),
                self.SEPARATOR
            )
        return super().format(record)
