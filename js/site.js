/* MSFT University — shared site JS */
(function () {
  "use strict";

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.setAttribute("aria-expanded", "false");
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) {
      if (links.classList.contains("open") && !links.contains(e.target)) {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ============================================================
     Easter eggs below. You found the source — that's egg #0. 🥚
     ============================================================ */

  /* ---------- Egg #1: the console ---------- */
  var css1 = "color:#0067b8;font-size:16px;font-weight:bold";
  var css2 = "color:#6e6e6e;font-size:12px";
  console.log("%c☁️  MSFT University — by Alex de Jong", css1);
  console.log(
    "%cSigninLogs\n| where UserPrincipalName == 'you'\n| where ResultType == 0  // you're in 😉\n| project Curiosity = 'level: expert'",
    "color:#7fba00;font-family:monospace;font-size:12px"
  );
  console.log("%cLike poking around? You'd probably enjoy the KQL Detective game → https://detective.kusto.io", css2);
  console.log("%cAchievements are live: explore, unlock, collect 1000G. Get-Achievements in the terminal shows your gamerscore.", css2);
  console.log("%cPsst: Konami code (↑↑↓↓←→←→BA) · logo squares 5× · press ~ for a terminal · type 'vista'.", css2);

  /* ---------- Egg #2: Konami code → BSOD ---------- */
  var konami = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
  var pos = 0;
  document.addEventListener("keydown", function (e) {
    if (e.key === konami[pos] || e.key.toLowerCase() === konami[pos]) {
      pos++;
      if (pos === konami.length) { pos = 0; bsod(); }
    } else {
      pos = e.key === konami[0] ? 1 : 0;
    }
  });

  window.__eggBsod = bsod;
  function bsod() {
    if (document.getElementById("egg-bsod")) return;
    var d = document.createElement("div");
    d.id = "egg-bsod";
    d.setAttribute("role", "dialog");
    d.style.cssText =
      "position:fixed;inset:0;z-index:99999;background:#0067b8;color:#fff;" +
      "font-family:'Segoe UI',sans-serif;display:flex;align-items:center;justify-content:center;cursor:pointer";
    d.innerHTML =
      '<div style="max-width:640px;padding:32px">' +
      '<div style="font-size:110px;line-height:1">:)</div>' +
      '<p style="font-size:22px;margin:24px 0 8px">Your PC is fine. This is just an easter egg.</p>' +
      '<p style="font-size:15px;opacity:.85">We\'re just collecting some curiosity info, and then you can keep browsing.<br>(0% complete — nothing is actually happening)</p>' +
      '<p style="font-size:13px;opacity:.7;margin-top:24px">Stop code: <b>USER_IS_A_KEYBOARD_NINJA</b><br>' +
      'What failed: nothing. You found the Konami code. Respect.</p>' +
      '<p id="egg-bsod-pct" style="font-size:15px;margin-top:16px">0% complete</p>' +
      '<p style="font-size:13px;opacity:.7;margin-top:16px">Click anywhere (or press Esc) to reboot.</p>' +
      "</div>";
    document.body.appendChild(d);
    window.__achieve && window.__achieve("bsod");
    var pct = 0;
    var t = setInterval(function () {
      pct = Math.min(100, pct + Math.floor(Math.random() * 17));
      var el = document.getElementById("egg-bsod-pct");
      if (el) el.textContent = pct + "% complete";
      if (pct >= 100) clearInterval(t);
    }, 400);
    function close() {
      clearInterval(t);
      d.remove();
      document.removeEventListener("keydown", esc);
    }
    d.addEventListener("click", close);
    function esc(e) { if (e.key === "Escape") close(); }
    document.addEventListener("keydown", esc);
  }

  /* ---------- Egg #3: click the logo 5× → Clippy ---------- */
  var mark = document.querySelector(".brand-mark");
  var clicks = 0, timer = null;
  if (mark) {
    mark.style.cursor = "pointer";
    mark.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      clicks++;
      clearTimeout(timer);
      timer = setTimeout(function () { clicks = 0; }, 2500);
      if (clicks >= 5) { clicks = 0; clippy(); }
    });
  }

  function clippy() {
    if (document.getElementById("egg-clippy")) return;
    var d = document.createElement("div");
    d.id = "egg-clippy";
    d.style.cssText =
      "position:fixed;right:24px;bottom:24px;z-index:99998;max-width:320px;" +
      "background:#fffbe6;border:2px solid #1b1b1b;border-radius:12px;padding:18px 20px;" +
      "box-shadow:0 12px 32px rgba(0,0,0,.25);font-family:'Segoe UI',sans-serif;font-size:14.5px;color:#1b1b1b";
    d.innerHTML =
      '<div style="font-size:40px;line-height:1;margin-bottom:8px">📎</div>' +
      "<p style='margin:0 0 12px'><b>It looks like you're trying to become Microsoft certified.</b><br>Would you like help with that?</p>" +
      '<div style="display:flex;gap:8px;flex-wrap:wrap">' +
      '<a href="training.html" style="background:#0067b8;color:#fff;padding:7px 14px;border-radius:6px;text-decoration:none;font-weight:600">Yes, obviously</a>' +
      '<button id="egg-clippy-no" style="background:none;border:1px solid #1b1b1b;padding:7px 14px;border-radius:6px;cursor:pointer;font-weight:600">No (I\'ll regret this)</button>' +
      "</div>";
    document.body.appendChild(d);
    window.__achieve && window.__achieve("clippy");
    document.getElementById("egg-clippy-no").addEventListener("click", function () {
      this.textContent = "Clippy never dies…";
      setTimeout(function () { d.remove(); }, 1200);
    });
  }
})();
