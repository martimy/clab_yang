#!/bin/bash

docker run --rm -it -v $(pwd)/.:/app/ martimy/yangtools:latest $@
