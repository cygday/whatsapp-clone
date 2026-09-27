# WhatsApp Clone Link Redirect

This Chrome extension routes WhatsApp group invite and channel links clicked on Facebook to WhatsApp Clone first. The app must be running at `http://127.0.0.1:8000/`, and you must be signed in. External WhatsApp invite links can be saved or opened in WhatsApp. Links to groups created inside this app can be joined and viewed here.

## Install in Chrome or Chromium

1. Start the app with `python manage.py runserver`.
2. Open `chrome://extensions`.
3. Turn on **Developer mode**.
4. Choose **Load unpacked** and select this `browser-extension` folder.
5. Reload the Facebook tab and click a WhatsApp group or channel link.

The extension only runs on Facebook domains listed in `manifest.json`. It does not read messages or group content. WhatsApp membership and browsing still happen on WhatsApp; this app cannot embed or import external WhatsApp content.