#!/bin/bash

# Set PYTHONPATH to include /app/my_module
export PYTHONPATH=/app/src

# Function to run the Python script
run_python_script() {
    python /app/src/pufo_twitter_bot/__main__.py -c 5 -s offenedaten --tweet
}

# Maximum number of attempts
max_attempts=5

# Counter for the attempts
attempts=0

# Get the current day of the week (1 = Monday, 7 = Sunday)
current_day=$(date +%u)

# Check if today is Friday (day 5)
if [ "$current_day" -ne 5 ]; then
    echo "Today is not Friday. Exiting."
    exit 0
fi

# Loop until the script succeeds or the maximum number of attempts is reached
while true; do
    attempts=$((attempts + 1))
    
    echo "Attempt $attempts..."
    
    # Run the Python script and capture its exit status
    run_python_script
    
    exit_status=$?
    
    if [ $exit_status -eq 0 ]; then
        echo "Script succeeded!"
        exit 0
    else
        echo "Script failed with exit code $exit_status."
        
        if [ $attempts -ge $max_attempts ]; then
            echo "Maximum number of attempts reached. Exiting."
            exit 1
        fi
        
        # Sleep for a while before the next attempt (adjust the sleep duration as needed)
        sleep 5
    fi
done
