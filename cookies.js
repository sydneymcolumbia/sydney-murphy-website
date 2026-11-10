/* Cookie consent banner — sets a single first-party cookie "sm_cookie_consent"
   with the visitor's choice ("accepted" or "declined"), valid for 180 days. */
(function () {
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

  if (getCookie(NAME)) return;

  var banner = document.createElement('div');
  banner.className = 'cookie-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-live', 'polite');
  banner.setAttribute('aria-label', 'Cookie notice');
  banner.innerHTML =
    '<p>This site uses a single cookie to remember your choice here. ' +
    'Fonts and icons load from Google Fonts and cdnjs, which may set their own cookies. ' +
    'No analytics or tracking.</p>' +
    '<div class="cookie-actions">' +
      '<button type="button" class="btn cookie-accept">Accept</button>' +
      '<button type="button" class="cookie-decline">Decline</button>' +
    '</div>';

  function close(choice) {
    setCookie(NAME, choice, DAYS);
    banner.classList.add('hide');
    setTimeout(function () { banner.remove(); }, 350);
  }

  banner.querySelector('.cookie-accept').addEventListener('click', function () { close('accepted'); });
  banner.querySelector('.cookie-decline').addEventListener('click', function () { close('declined'); });

  document.body.appendChild(banner);
  requestAnimationFrame(function () { banner.classList.add('show'); });
})();
