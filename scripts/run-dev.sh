#!/bin/bash

set -e

exec granian --reload --interface asgi --host 0.0.0.0 --port 8888 --log-config app/config/logging.json app.apis.api_v1:app 