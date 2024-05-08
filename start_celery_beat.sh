#!/bin/sh

# Define the path to the celerybeat-schedule file
SCHEDULE_FILE="celerybeat-schedule"

# Check if the file exists and delete it
if [ -f "$SCHEDULE_FILE" ]; then
    echo "Deleting existing celerybeat-schedule file..."
    rm "$SCHEDULE_FILE"
else
    echo "No celerybeat-schedule file found, starting celery-beat..."
fi

# Start celery-beat
exec celery -A django_celery_project beat -l info
