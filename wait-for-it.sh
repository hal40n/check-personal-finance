#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

TIMEOUT=15
QUIET=0
HOST=$1
PORT=$2
shift 2
CMD="$@"

if [[ $QUIET -eq 0 ]]; then
  echo "Waiting for $HOST:$PORT..."
fi

for i in $(seq $TIMEOUT); do
  nc -z $HOST $PORT > /dev/null 2>&1
  RESULT=$?
  if [[ $RESULT -eq 0 ]]; then
    if [[ $QUIET -eq 0 ]]; then
      echo "Connected to $HOST:$PORT"
    fi
    exec $CMD
    exit $?
  fi
  sleep 1
done

if [[ $QUIET -eq 0 ]]; then
  echo "Timed out waiting for $HOST:$PORT"
fi

exit 1
