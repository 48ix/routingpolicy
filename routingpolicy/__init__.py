"""Automatic Routing Policy Generation for 48 IX.

https://48ix.net

Copyright 2020 48 IX, Inc.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Standard Library
import logging
from logging import FileHandler, StreamHandler
from pathlib import Path

APP_DIR = Path("/etc/48ix-routingpolicy")

logger = logging.getLogger("routingpolicy")
logger.setLevel(logging.INFO)
log_file = Path.home() / "48ix-routingpolicy.log"
log_format = logging.Formatter(
    "[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s:%(lineno)s → %(message)s",
    datefmt="%Y%m%d %H:%M:%S",
)
file_handler = FileHandler(log_file)
term_handler = StreamHandler()
file_handler.setFormatter(log_format)
term_handler.setFormatter(log_format)
logger.addHandler(term_handler)
logger.addHandler(file_handler)
