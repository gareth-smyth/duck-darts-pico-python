#!/usr/bin/env sh

rshell mkdir /pyboard/lib
rshell mkdir /pyboard/src
rshell cp *.py /pyboard/
rshell cp src/* /pyboard/src/

if [ "$1" != "--no-deps" ]
then
  rshell cp lib/* /pyboard/lib/
fi
