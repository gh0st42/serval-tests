#!/bin/sh
for i in `ifconfig | grep "inet addr:10." | cut -d":" -f 2 | cut -d"." -f1,2,3`
do
servald scan $i.255
done
