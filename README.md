# Blogioma

**Simple Django blog application :D**

## Get started

1. Clone the repository and install the requirement packages:

```powershell
pip install -r requirements.txt
```

or via Poetry:

```powershell
poetry install
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


## Config

After this, you'll need to create and populate a `.env` file in the root directory. Blogioma has a feature that sends submitted user's form to email specified in `settings.py`. If you don't want to use this feature, you only need to populate the `SECRET_KEY` and `DEBUG` field. Otherwise, please populate all fields. For example:

```properties
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=0 OR 1

EMAIL_HOST=SMTP_SERVER
EMAIL_PORT=SMTP_PORT
EMAIL_HOST_USER=YOUR_EMAIL
EMAIL_HOST_PASSWORD=YOUR_EMAIL_APPLICATION_PASSWORD
EMAIL_USE_TLS=0 OR 1
EMAIL_USE_SSL=0 OR 1
```

| Key                  | Value                                                                                                                                               |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| SECRET_KEY           | This command can be used to generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. |
| DEBUG                | If true, runs debug mode. Default: 0 (false).                                                                                                       |
| EMAIL_HOST           | The host to use for sending email. E.g. `smtp.mail.ru`.                                                                                             |
| EMAIL_PORT           | Port to use for the SMTP server defined in `EMAIL_HOST`.                                                                                            |
| EMAIL_HOST_USER      | Username to use for the SMTP server defined in `EMAIL_HOST`.                                                                                        |
| EMAIL_HOST_PASSWORD  | Password to use for the SMTP server defined in `EMAIL_HOST`.                                                                                        |
| EMAIL_USE_TLS        | Whether to use a TLS (secure) connection when talking to the SMTP server. This is used for explicit TLS connections, generally on port 587. If you are experiencing hanging connections, use the implicit TLS setting `EMAIL_USE_SSL`. |
| EMAIL_USE_SSL        | Whether to use an implicit TLS (secure) connection when talking to the SMTP server. In most email documentation this type of TLS connection is referred to as SSL. It is generally used on port 465. If you are experiencing problems, use the explicit TLS setting `EMAIL_USE_TLS`. |



This is first my largest project, so I will be very happy when you star this repository or/and contribute with me. Good luck and have a nice day:D
