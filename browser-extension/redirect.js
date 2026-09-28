const whatsappHosts = new Set([
  'chat.whatsapp.com',
  'whatsapp.com',
  'www.whatsapp.com',
]);

function findWhatsAppLink(value, depth = 0) {
  if (depth > 3) return null;

  let candidate;
  try {
    candidate = new URL(value, document.baseURI);
  } catch {
    return null;
  }

  const host = candidate.hostname.toLowerCase();
  const path = candidate.pathname.replace(/^\/+|\/+$/g, '');
  const groupInvite = host === 'chat.whatsapp.com' && path.length > 0;
  const channelInvite = (host === 'whatsapp.com' || host === 'www.whatsapp.com')
    && /^channel\/[^/]+$/.test(path);

  if (candidate.protocol === 'https:' && (groupInvite || channelInvite)) {
    return candidate.href;
  }

  if (host.endsWith('.facebook.com')) {
    for (const key of ['u', 'url', 'href']) {
      const nested = candidate.searchParams.get(key);
      if (nested) return findWhatsAppLink(nested, depth + 1);
    }
  }

  return null;
}

document.addEventListener('click', (event) => {
  if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  if (!(event.target instanceof Element)) return;

  const anchor = event.target.closest('a[href]');
  if (!anchor) return;

  const whatsappUrl = findWhatsAppLink(anchor.href);
  if (!whatsappUrl) return;

  event.preventDefault();
  event.stopImmediatePropagation();
  chrome.storage.sync.get({ appUrl: 'https://whatsapp-clone-q1ad.onrender.com' }, ({ appUrl }) => {
    const relayUrl = new URL('/chat/links/open/', appUrl);
    relayUrl.searchParams.set('url', whatsappUrl);
    window.location.assign(relayUrl.href);
  });
}, true);