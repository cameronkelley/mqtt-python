# Send keyboard interrupt to screen session to quit omxplayer session
screen -X -S omx stuff "^C" >/dev/null 2>&1

sleep 2

# Send return to screen session in response to the omx exit prompt
# Send "exit" and a return to the stdin of the screen session to avoid creating duplicate screen sessions
screen -X -S omx stuff "\nexit\n" >/dev/null 2>&1