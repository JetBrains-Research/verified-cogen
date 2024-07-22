if [[ $(ps -o command= -p "$PPID" | awk '{print $1}') == '/usr/bin/login' ]]
then
    exec fish -l
fi
