# -*- coding: utf-8 -*-

"""Functions passed to our remote python-rq workers.  Must be in a separate module to __main__."""

import sys


def async_print(s):
    print(s)
    sys.stdout.flush()   # needed to make output appear in docker-compose log
    return True

