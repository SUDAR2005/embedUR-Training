#!/bin/bash

# declare variable for src, dst and ext
src=$1
dst=$2
ext=$3

# check dir exist
# 1. used command line arguments
if [ ! -d "$src" ]; then
    echo "src Folder $src is not given or doesn't exist"
    exit 1
fi

if [ ! -d "$dst" ]; then
    echo "dst Folder $dst doesn't exist, creating one"
    # 5. backup dir doesn't exist create if fails exit with error
    mkdir -p "$dst" || { echo "Creation failed..." ; exit 1;} 
fi

# check ext is valid
# 2. used globbing
# 4. store the names in array
mapfile -t files < <(find "$src" -type f -name "*$ext")

if [ "${#files[@]}" -eq 0 ]; then
    echo "no .$ext files found in source directory"
    exit 1
fi

echo "Files found:"
printf '%s\n' "${files[@]}"

echo "*************************--*****************************"
# 4. print file size and stats related to it
echo "Stats of files to be backed-up"
for file in "${files[@]}"; do
    stat -c "%n %s" "$file"
done

echo "*************************--*****************************"

# backup statistics
export BACKUP_COUNT=0
total_size=0

# 5. Backup files
for file in "${files[@]}"; do
    # Get just the filename without path for destination
    filename=$(basename "$file")
    dest_file="$dst/$filename"
    
    # check if the file exists already
    if [ -f "$dest_file" ]; then
        if [ "$file" -nt "$dest_file" ]; then
            cp "$file" "$dest_file"
            ((BACKUP_COUNT++))
            file_size=$(stat -c %s "$file")
            ((total_size+=file_size))
        else
            echo "$dest_file already exists and is up-to-date, skipping"
        fi
    else
        cp "$file" "$dest_file"
        ((BACKUP_COUNT++))
        file_size=$(stat -c %s "$file")
        ((total_size+=file_size))
    fi
done


report="$dst/backup_report.log"

{
    echo "Backup Summary Report"
    echo "total files processed: ${#files[@]}"
    echo "total files backed up: $BACKUP_COUNT"
    echo "total backup size: $total_size bytes"
    echo "backup directory: $dst"
    echo "date: $(date)"
} > "$report"

cat "$report"


echo "*************************--*****************************"
echo "Completed!!! report saved at $report"
echo "*************************--*****************************"