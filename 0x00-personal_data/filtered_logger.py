#!/usr/bin/env python3
"""Write a function called filter_datum"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for fld in fields:
        message = re.sub(
                rf'{fld}=[^{separator}]*', f"{fld}={redaction}", message)
    return message
