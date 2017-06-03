#!/usr/bin/env sh

#
# Enter Python virtualenv and start the python-rq worker
#

HW_PATH='/srv/themuse/hwaas'

cd $HW_PATH

. _venv/bin/activate

cd src
exec rq worker --quiet -c worker_settings

