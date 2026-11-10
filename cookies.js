/* Cookie consent banner + consent-gated Google Analytics.
   - One first-party cookie "sm_cookie_consent" stores the choice ("accepted" / "declined"), 180 days.
   - Google Analytics (GA4) loads ONLY after the visitor accepts. Declining or not choosing loads nothing.
   - Analytics is skipped on localhost so local previews never pollute the data. */
(function () {
  var GA_ID = 'G-WQMDTRY0ZZ'; // GA4 measurement ID
  var NAME = 'sm_cookie_consent';
  var DAYS = 180;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function setCookie(name, value, days) {
    var expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + encodeURIComponent(value) +
      '; expires=' + expires + '; path=/; SameSite=Lax' +
      (location.protocol === 'https:' ? '; Secure' : '');
  }

  function loadAnalytics() {
    if (window.__gaLoaded) return;
    if (!/^G-[A-Z0-9]+$/.test(GA_ID)) return;                       // placeholder ID, do nothing
    if (/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) return;
    window.__gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  var choice = getCookie(NAME);
  if (choice === 'accepted') loadAnalytics();
  if (choice) return;

  var banner = document.createElement('div');
  banner.className = 'cookie-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-live', 'polite');
  banner.setAttribute('aria-label', 'Cookie notice');
  banner.innerHTML =
    '<p>This site uses cookies for Google Analytics to understand which pages people read. ' +
    'Nothing loads unless you accept, and your choice is remembered for six months.</p>' +
    '<div class="cookie-actions">' +
      '<button type="button" class="btn cookie-accept">Accept</button>' +
      '<button type="button" class="cookie-decline">Decline</button>' +
    '</div>';

  function close(value) {
    setCookie(NAME, value, DAYS);
    if (value === 'accepted') loadAnalytics();
    banner.classList.add('hide');
    setTimeout(function () { banner.remove(); }, 350);
  }

  banner.querySelector('.cookie-accept').addEventListener('click', function () { close('accepted'); });
  banner.querySelector('.cookie-decline').addEventListener('click', function () { close('declined'); });

  document.body.appendChild(banner);
  requestAnimationFrame(function () { banner.classList.add('show'); });
})();
