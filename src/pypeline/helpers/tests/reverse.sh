#!/bin/bash
while read;
do
  echo $REPLY | sed '/\n/!G;s/\(.\)\(.*\n\)/&\2\1/;//D;s/.//'
done
