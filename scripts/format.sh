#!/bin/sh -e
set -x

ruff check webapp scripts --fix --unsafe-fixes
ruff format webapp scripts
