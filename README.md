# Blogioma

**Simple Django blog application :D**

## Get started

1. Clone the repository and install the requirement packages:

```powershell
pip install -r requirements-dev.txt
```

or via Poetry:

```powershell
poetry install --with dev
poetry shell
```

2. Create initial database and migrate:

```powershell
python manage.py migrate
```

3. Run the development server:

```powershell
python manage.py runserver
```


### Config

After this, you'll need to copy the contents from `.env.sample` to the new `.env` file:

```properties
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=0
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
INTERNAL_IPS=127.0.0.1,localhost,0.0.0.0

REDIS_HOST=127.0.0.1

EMAIL_HOST=YOUR_EMAIL_HOST
EMAIL_PORT=YOUR_EMAIL_PORT
EMAIL_HOST_USER=YOUR_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=YOUR_EMAIL_HOST_PASSWORD
EMAIL_USE_TLS=0
EMAIL_USE_SSL=1
```

| Key                         | Value                                                                                                                                               |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| SECRET_KEY                  | This command can be used to generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. |
| DEBUG                       | If true, runs debug mode. Default: 0 (false).                                                                                                       |
| ALLOWED_HOSTS, INTERNAL_IPS | A comma separated string. Default: 127.0.0.1,localhost,0.0.0.0.                                                                                     |
| REDIS_HOST                  | IP of Redis host. Default: 127.0.0.1. (Please, don't override this value when using Docker container.)                                              |
| EMAIL_HOST                  | The host to use for sending email. E.g. `smtp.mail.ru`.                                                                                             |
| EMAIL_PORT                  | Port to use for the SMTP server defined in `EMAIL_HOST`.                                                                                            |
| EMAIL_HOST_USER             | Username to use for the SMTP server defined in `EMAIL_HOST`.                                                                                        |
| EMAIL_HOST_PASSWORD         | Password to use for the SMTP server defined in `EMAIL_HOST`.                                                                                        |
| EMAIL_USE_TLS               | Whether to use a TLS (secure) connection when talking to the SMTP server. This is used for explicit TLS connections, generally on port 587. If you are experiencing hanging connections, use the implicit TLS setting `EMAIL_USE_SSL`. |
| EMAIL_USE_SSL               | Whether to use an implicit TLS (secure) connection when talking to the SMTP server. In most email documentation this type of TLS connection is referred to as SSL. It is generally used on port 465. If you are experiencing problems, use the explicit TLS setting `EMAIL_USE_TLS`. |


### Run via Docker

To run this project via Docker, you'll need to [create a `.env` file](#config) and run commands:

```bash
# For production
docker compose build --build-arg "ENV=PROD"
docker compose up -d

# For development
docker compose build --build-arg "ENV=DEV"
docker compose -f docker-compose-dev.yml up -d
```

This is first my largest project, so I will be very happy when you star this repository or/and contribute with me. Good luck and have a nice day:D
