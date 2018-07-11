#!/bin/bash

EXECUTABLE='node'
DEBUG='debug'
SCRIPT='background.js'
USER=`whoami`
APP_DIR='/home/geek/workspace/kids-library/node-app'

PIDFILE=$APP_DIR/ajab-gajab-background.pid
LOGFILE=$APP_DIR/ajab-gajab-background.log

start() {
    echo $(cat "$PIDFILE");
    if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE"); then
        echo 'Service already running' >&2
        return 1
    fi
    echo 'Starting service…' >&2
    local CMD="$EXECUTABLE $SCRIPT &> \"$LOGFILE\" & echo \$!"
    echo $CMD
    su -c "$CMD" $USER > "$PIDFILE"
    echo 'Service started' >&2
}

stop() {
    if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
        echo 'Service not running' >&2
        return 1
    fi
    echo 'Stopping service…' >&2
    kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
    echo 'Service stopped' >&2
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|uninstall}"
esac
