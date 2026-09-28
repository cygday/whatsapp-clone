# WhatsApp Clone Link Redirect

This Chrome extension routes WhatsApp group invite and channel links clicked on Facebook to WhatsApp Clone first. It is configured for `https://whatsapp-clone-q1ad.onrender.com/` by default. Sign in when prompted. External WhatsApp invite links can be saved in the app and opened in WhatsApp. Links to groups created inside this app can be joined and their messages browsed here.

## Install in Chrome or Chromium

1. On desktop Chrome or Chromium, open `chrome://extensions`.
2. Turn on **Developer mode**.
3. Choose **Load unpacked** and select this `browser-extension` folder.
4. Open the extension's **Details** page and confirm its app URL is `https://whatsapp-clone-q1ad.onrender.com`. The **Extension options** page lets you change it later.
5. Reload any Facebook tabs that were already open.
6. Click a Facebook WhatsApp group invite or channel link. Sign in to WhatsApp Clone if asked, then choose **Save link** on the invite page.
7. Visit the app's **Chats** page to browse saved links and groups. Click a saved external invite to continue to WhatsApp.

The extension only runs on Facebook domains listed in `manifest.json`. The app landing page lets you save the external link or continue to WhatsApp. Saved links and groups created in WhatsApp Clone are available from the app's Chats page. External WhatsApp groups remain on WhatsApp: the extension does not read messages, and this app cannot import or display their membership or content.