/* Homepage live bits: this year's teaching stats, next public events,
 * latest release notes, and the "install as app" hint.
 * Data: js/events.js (EVENTS, DELIVERED, COURSE_DAYS) and /api/whatsnew. */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var day = function (s) { return new Date(s + "T00:00:00"); };
  var EV = typeof EVENTS !== "undefined" ? EVENTS : [];
  var PAST = typeof DELIVERED !== "undefined" ? DELIVERED : [];
  var year = String(today.getFullYear());

  /* ---- stats: courses + countries this year (same rules as About) ---- */
  var done = EV.filter(function (e) { return e.date && day(e.date) <= today && e.date.slice(0, 4) === year; })
    .map(function (e) { return e.city || ""; })
    .concat(PAST.filter(function (e) { return String(e.month || "").slice(0, 4) === year; }).map(function (e) { return e.city || ""; }));
  if (done.length) {
    var countries = {};
    done.forEach(function (c) { if (c && !/^online/i.test(c)) countries[c.split(",").pop().trim()] = 1; });
    $("home-courses").textContent = done.length;
    $("home-courses-label").textContent = "Courses delivered in " + year;
    var n = Object.keys(countries).length;
    if (n) { $("home-countries").textContent = n; $("home-countries-label").textContent = "Countries in " + year; }
  }

  /* ---- next public events ---- */
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  function when(e) {
    var a = day(e.date), b = e.end ? day(e.end) : a;
    if (+a === +b) return a.getDate() + " " + MON[a.getMonth()];
    return a.getMonth() === b.getMonth() ? a.getDate() + "–" + b.getDate() + " " + MON[a.getMonth()]
      : a.getDate() + " " + MON[a.getMonth()] + " – " + b.getDate() + " " + MON[b.getMonth()];
  }
  function li(dateText, title, sub, href) {
    var l = document.createElement("li"), a = document.createElement(href ? "a" : "span");
    if (href) { a.href = href; if (/^https?:/.test(href)) { a.target = "_blank"; a.rel = "noopener"; } }
    var d = document.createElement("span"); d.className = "home-when"; d.textContent = dateText;
    var t = document.createElement("span"); t.className = "home-title"; t.textContent = title;
    var s = document.createElement("span"); s.className = "desc"; s.textContent = sub;
    a.appendChild(d); a.appendChild(t); a.appendChild(s); l.appendChild(a); return l;
  }
  var next = EV.filter(function (e) {
    return e.date && day(e.date) > today && !e.soldout && !/\(internal\)/i.test(e.title || "");
  }).sort(function (a, b) { return a.date < b.date ? -1 : 1; }).slice(0, 3);
  var evList = $("home-events-list");
  if (next.length) next.forEach(function (e) { evList.appendChild(li(when(e), e.title, [e.venue, e.city].filter(Boolean).join(" · "), e.url || "events.html")); });
  else { var x = document.createElement("li"); x.className = "desc"; x.textContent = "New dates are being planned — check the events page or book a private course."; evList.appendChild(x); }

  /* ---- latest release notes ---- */
  var nl = $("home-news-list");
  fetch("/api/whatsnew").then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (items) {
    if (!items || !items.length) throw 0;
    nl.innerHTML = "";
    items.slice(0, 4).forEach(function (it) {
      var src = String(it.source || "").replace(/^Microsoft (?!365)/, "");
      nl.appendChild(li(src, it.title, it.month + (it.stage ? " · " + it.stage : ""), it.link));
    });
  }).catch(function () {
    nl.innerHTML = "";
    var x = document.createElement("li"); x.className = "desc";
    x.textContent = "Copilot, Defender, Sentinel and Purview release notes and the Microsoft 365 roadmap — updated automatically.";
    nl.appendChild(x);
  });

  /* ---- install hint ---- */
  var inst = $("home-install");
  if (inst) {
    if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) { inst.parentNode.style.display = "none"; }
    inst.addEventListener("click", function (e) {
      e.preventDefault();
      var ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
      alert(ios
        ? "On iPhone or iPad: tap the Share button in Safari, then \"Add to Home Screen\"."
        : "In Chrome or Edge: open the browser menu and choose \"Install Microsoft University\" (or \"Apps → Install this site as an app\"). On Android: menu → \"Add to Home screen\".");
    });
  }
})();
