#!/bin/bash
if [ ${ENV} = "PROD" ]; then
    python manage.py collectstaic --noinput
fi

python manage.py migrate
