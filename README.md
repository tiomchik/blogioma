# Blogioma

**Simple Django blog application :D**

## Get started

1. Clone the repository and install the requirement packages:

for Windows:

```powershell
pip install -r requirements.txt
```

for MacOs and Linux:

```powershell
pip3 install -r requirements.txt
```

2. Create initial database and migrate:

for Windows:

```powershell
py manage.py migrate
```

for MacOs and Linux:

```powershell
python3 manage.py migrate
```

3. Run the development server:

for Windows:

```powershell
py manage.py runserver
```

for MacOs and Linux:

```powershell
python3 manage.py runserver
```


## Config

Blogioma has a feedback function that sends submitted user's form to email specified in `settings.py`. If you wanna use this feature, then you need to create and populate `.env` file in root dir. Example:

```properties
EMAIL_HOST=SMTP_SERVER
EMAIL_PORT=SMTP_PORT
EMAIL_HOST_USER=YOUR_EMAIL
EMAIL_HOST_PASSWORD=YOUR_EMAIL_APPLICATION_PASSWORD
EMAIL_USE_TLS=0 OR 1
EMAIL_USE_SSL=0 OR 1
```

| Key                  | Value                                                                                                                                               |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| EMAIL_HOST           | The host to use for sending email. E.g. `smtp.mail.ru`.                                                                                             |
| EMAIL_PORT           | Port to use for the SMTP server defined in `EMAIL_HOST`.                                                                                            |
| EMAIL_HOST_USER      | Username to use for the SMTP server defined in `EMAIL_HOST`.                                                                                        |
| EMAIL_HOST_PASSWORD  | Password to use for the SMTP server defined in `EMAIL_HOST`.                                                                                        |
| EMAIL_USE_TLS        | Whether to use a TLS (secure) connection when talking to the SMTP server. This is used for explicit TLS connections, generally on port 587. If you are experiencing hanging connections, use the implicit TLS setting `EMAIL_USE_SSL`. |
| EMAIL_USE_SSL        | Whether to use an implicit TLS (secure) connection when talking to the SMTP server. In most email documentation this type of TLS connection is referred to as SSL. It is generally used on port 465. If you are experiencing problems, use the explicit TLS setting `EMAIL_USE_TLS`. |



This is first my largest project, so I will be very happy when you star this repository or/and contribute with me. Good luck and have a nice day:D
