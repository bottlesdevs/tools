#!/bin/bash

# get distro name
distro=`cat /etc/os-release | grep "^ID=" | cut -d'=' -f2 | tr -d '"'`

# display usage if no argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./check-package-support.sh <package format> (e.g. flatpak, snap, dpkg, ..)"
    exit 1
fi

# check for binary
if [ -z "$(which $1)" ]; then
    echo -e "\e[1m$1\e[0m is not available in your system ($distro)"
else
    echo -e "\e[1m$1\e[0m is available in your system ($distro)"
fi