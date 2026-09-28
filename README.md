# WhatsApp Clone

A Django starter for account registration, private conversations, and member-managed group chats. It uses SQLite by default for local development and can use a hosted PostgreSQL database through `DATABASE_URL`.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and create an account. To administer the local database, create an administrator with `python manage.py createsuperuser` and visit `/admin/`.

## Use hosted PostgreSQL

Create a free PostgreSQL database with a hosting provider such as [Neon](https://neon.tech/), then set `DATABASE_URL` to the connection URL provided by the host. Keep this URL secret and do not commit it to the repository. For example, on Linux or macOS:

```bash
export DATABASE_URL='postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require'
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Run `migrate` against the hosted database before starting the app. If `DATABASE_URL` is not set, the app continues to use the local `db.sqlite3` file.

## Route Facebook WhatsApp Links Through the App

Load the unpacked Chrome/Chromium extension from `browser-extension/` at `chrome://extensions` (enable **Developer mode**, then select **Load unpacked**). The extension targets `https://whatsapp-clone-q1ad.onrender.com/` by default. Reload Facebook, click a WhatsApp group invite or channel link, and choose **Save link** after signing in. Saved links and groups created in WhatsApp Clone can be browsed from its Chats page. See [browser-extension/README.md](browser-extension/README.md) for details.

Groups created in WhatsApp Clone can be joined and viewed here using the app's group invite links. External WhatsApp group/channel links still open in WhatsApp; this app cannot display or import their content. The extension works in desktop Chrome/Chromium on the listed Facebook domains and cannot intercept links opened inside the Facebook mobile app.

## Tests

```bash
python manage.py test accounts chat groups
```

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS` before deploying. The included settings are for local development, not production.