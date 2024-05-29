#!/bin/bash

USER="admin"
PASSWORD="NokiaSrl1!"

COMMANDS="$@"

docker run -v $(pwd)/.:/files --net clab --rm ghcr.io/openconfig/gnmic \
 -u $USER -p $PASSWORD --skip-verify -e json_ietf $COMMANDS
