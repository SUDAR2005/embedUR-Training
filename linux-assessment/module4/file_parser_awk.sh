#! /bin/bash

input=$1
output="output_awk.txt"

# faster than the loop based script for parsing
awk '/"frame.time"|"wlan.fc.type"|"wlan.fc.subtype"/' "$input" | tr -d "[:blank:]" > "$output"