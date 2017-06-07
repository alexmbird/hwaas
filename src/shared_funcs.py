# -*- coding: utf-8 -*-

"""Functions passed to our remote python-rq workers.  Must be in a separate module to __main__."""



def async_print(s):
    print(s)
    return True

