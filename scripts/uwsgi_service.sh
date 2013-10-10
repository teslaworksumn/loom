#!/bin/sh
exec uwsgi --chdir /root/loom --socket 127.0.0.1:3545 --module loom --callable app --enable-threads
