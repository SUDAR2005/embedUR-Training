#!/bin/bash

log_error() {
    echo "ERROR: $1"
    echo "ERROR: $1" >> error.log
    exit 1
}

search_by_keyword() {
    local base_dir="$1"
    local keyword="$2"

    for item in "$base_dir"/*; do
        # regular file
        if [[ -f "$item" ]]; then
            if [[ "$(basename "$item")" == *"$keyword"* ]]; then
                echo "Match found: $item"
            fi
        fi

        # sub directory recursion
        if [[ -d "$item" ]]; then
            search_by_keyword "$item" "$keyword"
        fi
    done
}

show_help() {
    cat <<- "EOF"
    Usage: $0 [OPTIONS]

    Options:
    -d <directory>   Directory to search recursively
    -k <keyword>     Keyword to search
    -f <file>        Search keyword in file
    --help           Show this help menu

    Examples:
    $0 -d logs -k error
    $0 -f script.sh -k TODO
    $0 --help
EOF
}

# validate the arguments
validate_inputs() {
    # check keyword is empty
    [[ -z "${KEYWORD}" ]] && log_error "Keyword cannot be empty" && exit 1
    # check dir do exist
    if [[ -n "${DIR}" && ! -d "${DIR}" ]]; then
        log_error "Directory not found: ${DIR}"
    fi

    if [[ -n "${FILE}" && ! -f "${FILE}" ]]; then
        log_error "File not found: $FILE"
    fi

}

search_in_file() {
    local file="$1"
    local keyword="$2"
    # using grep to find keyword exist
    if grep -q "${keyword}" <<< "$(cat "${file}")"; then
        echo "Keyword '${keyword}' found in file ${file}"
    else
        echo "Keyword '${keyword}' NOT found in file ${file}"
    fi
}

for arg in "$@"; do
    [[ "$arg" == "--help" ]] && show_help && exit 0
done

while getopts ":d:k:f:" opt; do
    case $opt in
        d) DIR="$OPTARG" ;;
        k) KEYWORD="$OPTARG" ;;
        f) FILE="$OPTARG" ;;
        \?) log_error "Invalid option: -$OPTARG" ;;
        :) log_error "Option -$OPTARG requires argument" ;;
    esac
done


validate_inputs

if [[ -n "$DIR" ]]; then
    echo "Searching directory '$DIR' for keyword '$KEYWORD'"
    search_by_keyword "$DIR" "$KEYWORD"
fi

if [[ -n "$FILE" ]]; then
    echo "Searching file '$FILE' for keyword '$KEYWORD'"
    search_in_file "$FILE" "$KEYWORD"
fi


echo "Script: $0"
echo "Total arguments: $#"
echo "Arguments: $*"

exit 0