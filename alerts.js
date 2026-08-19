/*
 * NWS heat-alert banner for heatguide.planetdetroit.org
 *
 * Plain English: when the page loads, ask the National Weather Service whether a
 * heat advisory/watch/warning is active for Wayne, Oakland or Macomb County. If yes,
 * show a colored strip at the very top of the page. If no — or if the request fails,
 * times out, or the phone has no JavaScript — show NOTHING. The page never depends on this.
 *
 * Data: https://api.weather.gov/alerts/active?zone=MIZ076,MIZ069,MIZ070 (free, no key, CORS ok)
 * Zones: MIZ076 Wayne · MIZ069 Oakland · MIZ070 Macomb (NWS Detroit/Pontiac office)
 */
(function () {
  'use strict';

  var ZONES = 'MIZ076,MIZ069,MIZ070';
  var API = 'https://api.weather.gov/alerts/active?zone=' + ZONES;
  var TIMEOUT_MS = 6000;

  // Most serious first. Matched by substring so legacy names ("Excessive Heat Warning") work.
  var LEVELS = [
    { match: /heat warning/i, level: 'warning' },
    { match: /heat advisory/i, level: 'advisory' },
    { match: /heat watch/i, level: 'watch' }
  ];

  var TEXT = {
    en: {
      'Extreme Heat Warning': 'Extreme Heat Warning',
      'Excessive Heat Warning': 'Excessive Heat Warning',
      'Heat Advisory': 'Heat Advisory',
      'Extreme Heat Watch': 'Extreme Heat Watch',
      'Excessive Heat Watch': 'Excessive Heat Watch',
      area: 'in effect for Metro Detroit',
      until: 'until',
      source: 'National Weather Service',
      more: 'Details'
    },
    es: {
      'Extreme Heat Warning': 'Alerta de calor extremo',
      'Excessive Heat Warning': 'Alerta de calor excesivo',
      'Heat Advisory': 'Aviso de calor',
      'Extreme Heat Watch': 'Vigilancia de calor extremo',
      'Excessive Heat Watch': 'Vigilancia de calor excesivo',
      area: 'vigente para el área metropolitana de Detroit',
      until: 'hasta',
      source: 'Servicio Meteorológico Nacional',
      more: 'Detalles'
    }
  };

  function levelOf(event) {
    for (var i = 0; i < LEVELS.length; i++) if (LEVELS[i].match.test(event || '')) return LEVELS[i];
    return null;
  }

  // Pick the single most serious, still-active heat alert from an NWS response.
  // Returns null for anything that isn't a clear heat alert — never throws.
  function pickHeatAlert(payload, now) {
    try {
      var feats = (payload && payload.features) || [];
      var best = null, bestRank = 99;
      var t = (now || new Date()).getTime();
      for (var i = 0; i < feats.length; i++) {
        var p = feats[i] && feats[i].properties;
        if (!p) continue;
        var lv = levelOf(p.event);
        if (!lv) continue;
        var ends = p.ends || p.expires;
        if (ends && !isNaN(Date.parse(ends)) && Date.parse(ends) < t) continue; // already over
        var rank = LEVELS.indexOf(lv);
        if (rank < bestRank) { best = feats[i]; bestRank = rank; }
      }
      return best;
    } catch (e) { return null; }
  }

  function fmtTime(iso, lang) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    try {
      return d.toLocaleString(lang === 'es' ? 'es-US' : 'en-US',
        { weekday: 'short', hour: 'numeric', minute: '2-digit', timeZone: 'America/Detroit' });
    } catch (e) { return ''; }
  }

  // Build the words for the banner in the requested language.
  function bannerText(alert, lang) {
    var t = TEXT[lang] || TEXT.en;
    var p = alert.properties || {};
    var name = t[p.event] || p.event || 'Heat alert';
    var lv = levelOf(p.event);
    var ends = p.ends || p.expires;
    var when = ends ? fmtTime(ends, lang) : '';
    return {
      level: lv ? lv.level : 'advisory',
      title: name,
      detail: t.area + (when ? ' ' + t.until + ' ' + when : '') + ' — ' + t.source,
      more: t.more,
      url: 'https://www.weather.gov/dtx/' // NWS Detroit/Pontiac office page
    };
  }

  function render(alert) {
    var box = document.getElementById('heat-alert');
    if (!box || !alert) return;
    var lang = (document.documentElement.lang || 'en').slice(0, 2);
    var b = bannerText(alert, lang);
    box.className = 'heat-alert heat-alert-' + b.level;
    box.innerHTML = '';
    var strong = document.createElement('strong'); strong.textContent = '⚠️ ' + b.title + ' ';
    var span = document.createElement('span'); span.textContent = b.detail + ' · ';
    var a = document.createElement('a'); a.href = b.url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = b.more;
    box.appendChild(strong); box.appendChild(span); box.appendChild(a);
    box.hidden = false;
    if (window.gtag) gtag('event', 'heat_alert_shown', { alert_event: alert.properties.event });
  }

  function load() {
    if (!window.fetch) return;
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, TIMEOUT_MS);
    fetch(API, {
      signal: ctrl ? ctrl.signal : undefined,
      headers: { 'Accept': 'application/geo+json', 'X-Requested-With': 'heatguide.planetdetroit.org' }
    })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) { clearTimeout(timer); render(pickHeatAlert(data)); })
      .catch(function () { clearTimeout(timer); /* stay silent — page works without the banner */ });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { pickHeatAlert: pickHeatAlert, bannerText: bannerText }; // for tests
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
})();
