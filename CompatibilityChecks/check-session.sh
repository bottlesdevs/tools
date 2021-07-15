#!/bin/bash

IS_X11=false
IS_WAYLAND=false

# if XDG_SESSION_TYPE is set, check output
if [ -n "${XDG_SESSION_TYPE}" ]; then

    # check if session is x11, wayland or unknown
    if [ "$XDG_SESSION_TYPE" = "x11" ]; then
        IS_X11=true
    elif [ "$XDG_SESSION_TYPE" = "wayland" ]; then
        IS_WAYLAND=true
    fi

# check if DISPLAY is set, if so, assume X11
elif [ -n "${DISPLAY}" ]; then
    IS_X11=true

# check if WAYLAND_DISPLAY is set, if so, assume wayland
elif [ -n "$WAYLAND_DISPLAY" ]; then
    IS_WAYLAND=true

# then we are going to check trought the process list
else
    if pgrep "x11" >/dev/null; then
        IS_X11=true
    fi
    if pgrep "wayland" >/dev/null; then
        IS_WAYLAND=true
    fi
fi

if [ "$IS_X11" = true ]; then
    echo -e "You are running a \e[1mx11\e[0m session"
elif [ "$IS_WAYLAND" = true ]; then
    echo -e "You are running a \e[1mWayland\e[0m session"
else
    echo "Unknown session type"
fi