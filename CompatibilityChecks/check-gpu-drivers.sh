#!/bin/bash

HAS_AMD=false
HAS_INTEL=false
HAS_NVIDIA=false
HAS_NOUVEAU=false

# AMD - check if gpu is amd
if ! [ "$(lspci | grep AMD)" = "" ]; then
    HAS_AMD=true
    echo -e "\e[1mAMD\e[0m graphics driver detected"
fi

# Intel - check if gpu is intel
if ! [ "$(lspci | grep Intel)" = "" ]; then
    HAS_INTEL=true
    echo -e "\e[1mIntel\e[0m graphics driver detected"
fi

# Nvidia - check if gpu is nvidia
if ! [ "$(lspci | grep NVIDIA)" = "" ]; then
    HAS_NVIDIA=true
    echo -e "\e[1mNVIDIA\e[0m graphics driver detected"
fi

# Nouveau - check if gpu is nouveau
if ! [ "$(lspci | grep Nouveau)" = "" ]; then
    HAS_NOUVEAU=true
    echo -e "\e[1mNouveau\e[0m graphics driver detected"
fi

if [ "$HAS_AMD" = true ] && [ "$HAS_NVIDIA" = true ] || 
   [ "$HAS_INTEL" = true ] && [ "$HAS_NVIDIA" = true ] || 
   [ "$HAS_INTEL" = true ] && [ "$HAS_AMD" = true ]; then
    echo -e "Found a \e[1mPRIME\e[0m configuration. <https://wiki.archlinux.org/title/PRIME>"
fi

# Check if the system has a supported graphics driver
if [ "$HAS_AMD" = true ] || 
   [ "$HAS_INTEL" = true ] || 
   [ "$HAS_NVIDIA" = true ] || 
   [ "$HAS_NOUVEAU" = true ]; then
    exit 0
else
    echo "No supported graphics driver detected"
    exit 1
fi
