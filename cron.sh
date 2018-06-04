#!/usr/bin/env bash
cp ./cebulobot.cron /etc/cron.d/cebulobot
service cron restart
