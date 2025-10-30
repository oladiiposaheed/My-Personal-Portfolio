#!/bin/bash

# Wait for database to be ready (if using PostgreSQL)
if [ "$DB_LIVE" = "True" ] || [ "$DB_LIVE" = "true" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn porfolio.wsgi:application --bind 0.0.0.0:$PORT --workers 3