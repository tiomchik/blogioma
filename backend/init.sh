#!/bin/bash
if [[ ${ENV} = "PROD" ]]; then
    python manage.py collectstatic --noinput
fi

python manage.py migrate
