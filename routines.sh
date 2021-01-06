# methods
function get_window_id {
	while : ; do
	    sleep 0.2
	    set +e
	    WINDOW_ID=$(xdotool search --name "$1")
	    set -e
	    [[ -z $WINDOW_ID ]] || break
	done
	echo "$WINDOW_ID"
}

function execute_routine {
	xdotool windowfocus $1
	xdotool key ${@:2}
	echo "Routine: ${@:2} executed successfully!"
}

# routine execution
wine setup.exe &

# First dialog
WINDOW_ID=$(get_window_id "Installer*")
execute_routine "$WINDOW_ID" Tab space
sleep 2

# Second dialog
WINDOW_ID=$(get_window_id "Notepad++*")
execute_routine "$WINDOW_ID" space Return Return Return Return
sleep 2.5
execute_routine "$WINDOW_ID" space Return
