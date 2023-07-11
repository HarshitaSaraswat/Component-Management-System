#!/usr/bin/zsh

set -e
source .venv/bin/activate

set -a
export $(xargs <.env)
set +a

flask run

deactivate
