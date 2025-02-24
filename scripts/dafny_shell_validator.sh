#!/bin/bash

var1=$1;
var2=$2;
var3=$3;

echo "$var1" > $var3;
~/Nagini-Convertion/Binaries/Dafny validate $var3;
echo "module Gen {"
echo -e "$var2"
echo "}"
cat $var3
