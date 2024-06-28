FROM python:3.11

COPY requirements.txt requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .

EXPOSE 8000

RUN python manage.py migrate
