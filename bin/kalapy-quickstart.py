#!/usr/bin/env python
import sys
from kalapy import admin

if __name__ == "__main__":
    args = ['startproject'] + sys.argv[1:]
    admin.execute_command(args)

