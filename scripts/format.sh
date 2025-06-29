#!/bin/sh -e
set -x

ruff check src scripts --fix --unsafe-fixes
ruff format src scripts
