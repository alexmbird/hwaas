#!/usr/bin/env sh

#
# Enter Python virtualenv and start the `hwserver` service
#

HW_PATH='/srv/themuse/hwaas'

cd $HW_PATH

. _venv/bin/activate

cd src
exec python3 hw-client.py

