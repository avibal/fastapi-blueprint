#!/bin/bash
nohup python main.py > flask.log 2>&1 &
disown