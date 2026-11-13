"""
Adapted from https://stackoverflow.com/a/51028921/14485040

This script has to be included in the `notebooks` directory and
has to be imported (first line) in every notebook that uses
scripts/data from directories relative to the root directory of
the project.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(".."))
# `..` indicate a relative path to root directory
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
