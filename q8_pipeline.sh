#!/bin/bash

# Assignment 5, Question 8: Pipeline Automation Script
# Run the clinical trial data analysis pipeline

LOGFILE="reports/pipeline_log.txt"
echo "Starting clinical trial data pipeline..." > "$LOGFILE"
date >> "$LOGFILE"

run_notebook() {
    NOTEBOOK=$1
    echo "Running $NOTEBOOK..." >> "$LOGFILE"
    jupyter nbconvert --execute --to notebook "$NOTEBOOK" --output "$NOTEBOOK" >> "$LOGFILE" 2>&1

    if [ $? -ne 0 ]; then
        echo "❌ ERROR: $NOTEBOOK failed. Stopping pipeline." >> "$LOGFILE"
        echo "Pipeline failed. Check $LOGFILE for details."
        exit 1
    else
        echo "✅ Successfully completed $NOTEBOOK." >> "$LOGFILE"
    fi
}


run_notebook "q4_exploration.ipynb"
run_notebook "q5_missing_data.ipynb"
run_notebook "q6_transformation.ipynb"
run_notebook "q7_aggregation.ipynb"


echo "Pipeline complete!" >> "$LOGFILE"
date >> "$LOGFILE"
echo "✅ All notebooks executed successfully. Log saved to $LOGFILE."
