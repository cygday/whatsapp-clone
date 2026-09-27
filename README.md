# WhatsApp Clone

A Django starter for account registration, private conversations, and member-managed group chats. The app uses SQLite by default, so it runs locally without a separate database service.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and create an account. To administer the local database, create an administrator with `python manage.py createsuperuser` and visit `/admin/`.

## Route Facebook WhatsApp Links Through the App

With the local server running and your account signed in, load the unpacked Chrome/Chromium extension from `browser-extension/` at `chrome://extensions` (enable **Developer mode**, then select **Load unpacked**). Reload Facebook and click a WhatsApp group invite or channel link. WhatsApp Clone opens a page where you can save the external link or continue to WhatsApp. See [browser-extension/README.md](browser-extension/README.md) for details.

Groups created in WhatsApp Clone can be joined and viewed here using the app's group invite links. External WhatsApp group/channel links still open in WhatsApp; this app cannot display or import their content. The extension works in desktop Chrome/Chromium on the listed Facebook domains and cannot intercept links opened inside the Facebook mobile app.

## Tests

```bash
python manage.py test accounts chat groups
```

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS` before deploying. The included settings are for local development, not production.