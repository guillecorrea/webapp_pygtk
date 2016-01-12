#!/bin/bash
./server.py &
SERVER=$!
./webapp.py
kill -9 $SERVER 