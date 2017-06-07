#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rq import Queue
from redis import Redis
import os, time

from shared_funcs import async_print

DELAY=1




if __name__ == '__main__':
    print("Client starting up")
    redis_conn = Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/1'))
    q = Queue(connection=redis_conn)  # no args implies the default queue
    while True:
        job = q.enqueue(async_print, 'hello world')
        time.sleep(DELAY)  # wait a while, until the worker is finished
        print("Completion: %s" % (job.result,))
