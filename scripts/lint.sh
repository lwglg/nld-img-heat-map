#!/usr/bin/env bash

set -e
set -x

mypy webapp
ruff check webapp
ruff format webapp --check
