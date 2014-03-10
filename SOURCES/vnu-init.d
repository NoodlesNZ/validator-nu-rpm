#!/bin/sh
#
#   /etc/init.d/validator-nu
#
#   Starts and stops validator-nu as a "daemon".
#
# chkconfig: 2345 30 70
# description: Starts and stops validator-nu as a daemon.

# The name of this service
NAME=validator-nu

### Start Configuration Options ###

# The PID file
PID_FILE=/var/run/validator-nu.pid

# The command to daemonize
DAEMON="java -cp /opt/validator-nu/vnu.jar nu.validator.servlet.Main 8888 > /var/log/validator/validator-nu 2>&1 &"


### End Configuration Options ###

. /etc/init.d/functions

start() {

  echo -n $"Starting $NAME: "

  daemon --check $NAME --user validator --pidfile $PID_FILE $DAEMON

  RETVAL=$?

  if [ $RETVAL -ne 0 ]; then
    echo_failure
    echo
  else
    PID=$(ps aux | grep -m 1 "nu.validator.servlet" | awk '{print $2}')
    echo -n $PID > $PID_FILE
    echo_success
    echo
  fi
  return $RETVAL
}

stop () {
  echo -n $"Stopping $NAME: "
  killproc -p $PID_FILE $NAME
  RETVAL=$?
  echo
  return $RETVAL
}

restart () {
  stop
  start
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status -p $PID_FILE $NAME
    ;;
  restart)
    restart
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
    exit 2
    ;;
esac

exit $?
