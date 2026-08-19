#!/usr/bin/env node
// Tests for the NWS heat-alert banner logic in /alerts.js.
// Plain-English: given what the weather service returns, do we show the right
// banner (or none)? Run with: node tests/test_alerts.js
const { pickHeatAlert, bannerText } = require('../alerts.js');
let fails = 0;
function check(name, cond, detail) {
  console.log(`  ${cond ? 'PASS' : 'FAIL'}  ${name}${cond ? '' : '  ' + (detail || '')}`);
  if (!cond) fails++;
}
const mk = (event, ends, extra) => ({ properties: Object.assign({ event, ends, expires: ends, headline: event + ' issued', areaDesc: 'Wayne, MI' }, extra) });

// No alerts → no banner.
check('No features → null', pickHeatAlert({ features: [] }) === null);
// Garbage / API-down shapes → null, never throw.
check('Missing features → null', pickHeatAlert({}) === null);
check('null payload → null', pickHeatAlert(null) === null);
// Non-heat alerts (e.g., thunderstorm) are ignored.
check('Thunderstorm only → null', pickHeatAlert({ features: [mk('Severe Thunderstorm Warning', '2030-07-01T20:00:00-04:00')] }) === null);
// Heat alerts are recognized, including the legacy "Excessive Heat" name.
check('Heat Advisory → picked', pickHeatAlert({ features: [mk('Heat Advisory', '2030-07-01T20:00:00-04:00')] }).properties.event === 'Heat Advisory');
check('Excessive Heat Warning (legacy name) → picked', pickHeatAlert({ features: [mk('Excessive Heat Warning', '2030-07-01T20:00:00-04:00')] }) !== null);
// When several heat alerts exist, the most serious one wins: Warning > Advisory > Watch.
const multi = { features: [mk('Extreme Heat Watch', '2030-07-02T20:00:00-04:00'), mk('Heat Advisory', '2030-07-01T20:00:00-04:00'), mk('Extreme Heat Warning', '2030-07-01T20:00:00-04:00')] };
check('Warning beats Advisory beats Watch', pickHeatAlert(multi).properties.event === 'Extreme Heat Warning');
// Alerts that have already ended are ignored (NWS occasionally lags).
check('Expired alert → null', pickHeatAlert({ features: [mk('Heat Advisory', '2000-01-01T00:00:00-04:00')] }, new Date('2030-01-01')) === null);
// Banner wording, English and Spanish, with an "until" time.
const a = mk('Heat Advisory', '2030-07-01T20:00:00-04:00');
const en = bannerText(a, 'en'), es = bannerText(a, 'es');
check('EN text names the alert', /Heat Advisory/.test(en.title));
check('EN text has "until"', /until/i.test(en.detail), en.detail);
check('ES text names the alert in Spanish', /Aviso de calor/.test(es.title), es.title);
check('ES text has "hasta"', /hasta/i.test(es.detail), es.detail);
check('Unknown heat event still renders (falls back to NWS name)', /Something Heat/.test(bannerText(mk('Something Heat Thing', '2030-07-01T20:00:00-04:00'), 'es').title));
// Severity class drives color: warning = red, advisory/watch = amber.
check('Warning → level "warning"', bannerText(mk('Extreme Heat Warning', '2030-07-01T20:00:00-04:00'), 'en').level === 'warning');
check('Advisory → level "advisory"', en.level === 'advisory');

console.log();
if (fails) { console.log(`${fails} check(s) failed`); process.exit(1); }
console.log('All alert-logic checks passed');
