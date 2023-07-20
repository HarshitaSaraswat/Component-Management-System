#!/usr/bin/zsh

set -e
source .venv/bin/activate

flask run

deactivate
