#!/bin/bash

### RUN WITH THIS COMMAND ###
### ./slowhttp_long.sh <URL> -c 65000 -H

# CHECK IF SLOWHTTPTEST IS INSTALLED
if ! command -v slowhttptest &> /dev/null; then
    echo "Error: slowhttptest is not installed
    exit 1
fi

# CHECK FOR REQUIRED URL ARGUMENT
if [ -z "$1" ]; then
    echo "Usage: $0 <url> [additional_args]"
    echo "Example: $0 http://example.com -c 100 -H"
    exit 1
fi

URL=$1
shift
ARGS=$@

echo "Starting slowhttptest against $URL. Press Ctrl+C to stop."

# LOOP INDEFINATELY
while true; do

    #EXECUTE SLOWHTTPTEST WITH PROVIDED ARGUMENTS
    slowhttptest -u "$URL" $ARGS

    # OPTIONAL: BRIEF PAUSE TO PREVENT RAPID-FIRE RESTARTS IF THE COMMAND FAILS
    sleep 1
done

