#!/bin/bash

python3 -m venv .venv --prompt onboarding_buddy
. .venv/bin/activate \
    && pip3 install --upgrade pip wheel \
#    && pip3 install -r requirements.txt
