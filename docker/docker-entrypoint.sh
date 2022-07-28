#!/bin/sh

set -e

. /venv/bin/activate

exec env ENV=PROD python main.py