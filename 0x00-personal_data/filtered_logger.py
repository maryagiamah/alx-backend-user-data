#!/usr/bin/env python3
"""Write a function called filter_datum"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    for fld in fields:
        message = re.sub(
                rf'{fld}=[^{separator}]*', f"{fld}={redaction}", message)
    return message
