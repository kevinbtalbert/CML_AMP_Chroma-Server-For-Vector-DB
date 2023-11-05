#!/bin/bash
# Script to add three lines to the top of a Python file

# Path to the Python file
FILE="/home/cdsw/.local/lib/python3.10/site-packages/chromadb/__init__.py"

# Temporary file to store the new content
TEMP_FILE=$(mktemp)

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "The specified file does not exist."
    exit 1
fi

# The three lines to be added
LINE1="__import__('pysqlite3')"
LINE2="import sys"
LINE3="sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')"
LINE4="import logging"
LINE5="chroma_logger = logging.getLogger('chroma')"
LINE6="chroma_logger.setLevel(logging.CRITICAL)"

# Write the new lines to the temp file
echo "$LINE1" > "$TEMP_FILE"
echo "$LINE2" >> "$TEMP_FILE"
echo "$LINE3" >> "$TEMP_FILE"
echo "$LINE4" >> "$TEMP_FILE"
echo "$LINE5" >> "$TEMP_FILE"
echo "$LINE6" >> "$TEMP_FILE"

# Append the original file content to the temp file
cat "$FILE" >> "$TEMP_FILE"

# Replace the original file with the new file
mv "$TEMP_FILE" "$FILE"

echo "Lines added successfully."
