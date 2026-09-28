const defaultAppUrl = 'https://whatsapp-clone-q1ad.onrender.com';
const form = document.querySelector('#settings-form');
const appUrlInput = document.querySelector('#app-url');
const status = document.querySelector('#status');

chrome.storage.sync.get({ appUrl: defaultAppUrl }, ({ appUrl }) => {
  appUrlInput.value = appUrl;
});

form.addEventListener('submit', (event) => {
  event.preventDefault();

  let appUrl;
  try {
    appUrl = new URL(appUrlInput.value.trim());
  } catch {
    status.textContent = 'Enter a valid app URL.';
    return;
  }

  if (!['http:', 'https:'].includes(appUrl.protocol)) {
    status.textContent = 'Use an HTTP or HTTPS app URL.';
    return;
  }

  chrome.storage.sync.set({ appUrl: appUrl.origin }, () => {
    appUrlInput.value = appUrl.origin;
    status.textContent = 'Settings saved.';
  });
});