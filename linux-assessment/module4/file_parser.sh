#!/bin/bash
# input files
input="$1"
output="output.txt"

if [ ! -f "$input" ]; then
    echo "Type as  $0 <input_file>"
    exit 1
fi
# clear existing content
true > "$output"   
# loop through the input file, match cases and append to output file as per the format 
while IFS= read -r line; do
    case "$line" in
        *'"frame.time"'*)
            echo "$line" | tr -d "[:blank:]" >> "$output"
            ;;
        *'"wlan.fc.type"'*)
            echo "$line" | tr -d "[:blank:]" >> "$output"
            ;;
        *'"wlan.fc.subtype"'*)
            echo "$line" | tr -d "[:blank:]" >> "$output"
            ;;
    esac
done < "$input"
