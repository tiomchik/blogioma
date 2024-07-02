FROM python:3.11

WORKDIR /root/blogioma/

RUN pip install --upgrade pip
COPY requirements.txt requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .

EXPOSE 8000

RUN chmod u+x init.sh && ./init.sh
