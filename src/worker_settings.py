# -*- coding: utf-8 -*-


# I can't find any sign that `rq worker` accepts config via env vars, which is
# the easiest way to set things up with Docker.  Thus I've added this simple
# settings file to proxy them in.
# Plagiarized from http://python-rq.org/docs/workers/


import os


REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')

# You can also specify the Redis DB to use
# REDIS_HOST = 'redis.example.com'
# REDIS_PORT = 6380
# REDIS_DB = 3
# REDIS_PASSWORD = 'very secret'

# Queues to listen on
#QUEUES = ['high', 'normal', 'low']

# If you're using Sentry to collect your runtime exceptions, you can use this
# to configure RQ for it in a single step
#SENTRY_DSN = 'http://public:secret@example.com/1'
