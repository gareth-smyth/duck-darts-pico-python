#!/usr/bin/env sh

read -p "Enter your SSID: " ssid
read -p "Enter your WiFi Password: " pass

printf "SSID = \"%s\"\n" "${ssid}" > environment.py
printf "PASSWORD = \"%s\"\n" "${pass}" >> environment.py
