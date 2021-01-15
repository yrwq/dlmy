#!/usr/bin/env bash

if [[ ! $@ ]]; then
    python3 -m dlmy -h
else
    python3 -m dlmy $@
fi
