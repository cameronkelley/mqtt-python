# Send keyboard interrupt to screen session to quit omxplayer session
screen -X -S omx stuff "^C" >/dev/null 2>&1

sleep 2

# Send return to screen session in response to the omx exit prompt
# Send "exit" and a return to the stdin of the screen session to avoid creating duplicate screen sessions
screen -X -S omx stuff "\nexit\n" >/dev/null 2>&1

sleep 1

# Create a detached screen session called "omx"
# Send command to detached screen session calling camera script
screen -dmS omx bash -c '/root/omx_front_door.sh' >/dev/null 2>&1
