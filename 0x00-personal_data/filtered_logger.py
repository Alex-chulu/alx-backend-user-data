#!/usr/bin/env python3
import re

def filter_datum(fields, redaction, message, separator):
    return re.sub(r'(?<=\{}{})(.*?)(?=\{}|$)'.format(separator, 
    '|'.join(fields), separator), redaction, message)
