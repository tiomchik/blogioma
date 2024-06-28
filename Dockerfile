FROM python:3.11

COPY requirements.txt requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .

CMD ["python", "manage.py", "migrate"]
