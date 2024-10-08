#!/bin/bash
while true; do
    echo Try to upgrade database...
    flask db stamp head
    flask db migrate
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
