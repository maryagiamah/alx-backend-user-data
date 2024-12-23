#!/usr/bin/env python3
"""Write a function called filter_datum"""
import re
from typing import List
import logging
import mysql.connector
from os import environ


PII_FIELDS = ("email", "ssn", "password", "name", "phone")


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    for fld in fields:
        message = re.sub(
                rf'{fld}=[^{separator}]*', f'{fld}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """ takes no arguments and returns a logging.Logger object"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    hdlr = logging.StreamHandler()
    hdlr.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(hdlr)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """return this """
    config = {
            'user': environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
            'password': environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
            'host': environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
            'database': environ.get('PERSONAL_DATA_DB_NAME')
        }

    return mysql.connector.connect(**config)


def main():
    """main func"""

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    fld_nm = [col[0] for col in cur.description]

    logger = get_logger()

    for row in cur.fetchall():
        message = ' '.join([f'{fld}={col};' for col, fld in zip(row, fld_nm)])
        logger.info(message)

    cur.close()
    db.close()


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


if __name__ == '__main__':
    main()
