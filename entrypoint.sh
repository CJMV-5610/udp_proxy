#!/bin/bash

nslookup minetest
netcat -v -u -z minetest 30000
python3 -u udp_proxy.py 30000 20000
