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
      '<svg width="58" height="81" viewBox="0 0 100 140" aria-hidden="true" style="display:block;margin-bottom:8px;transform:rotate(-6deg)">' +
      '<g fill="none" stroke-linecap="round">' +
      '<path d="M30 128 L30 38 A20 20 0 0 1 70 38 L70 106 A14 14 0 0 1 42 106 L42 56 A8 8 0 0 1 58 56 L58 96" stroke="#6f7880" stroke-width="9"/>' +
      '<path d="M30 128 L30 38 A20 20 0 0 1 70 38 L70 106 A14 14 0 0 1 42 106 L42 56 A8 8 0 0 1 58 56 L58 96" stroke="#c8cdd2" stroke-width="3.5"/>' +
      '</g>' +
      '<path d="M26 8 Q35 2 44 7" stroke="#1b1b1b" stroke-width="4" fill="none" stroke-linecap="round"/>' +
      '<path d="M56 7 Q65 2 74 8" stroke="#1b1b1b" stroke-width="4" fill="none" stroke-linecap="round"/>' +
      '<ellipse cx="38" cy="26" rx="10.5" ry="13.5" fill="#fff" stroke="#1b1b1b" stroke-width="3"/>' +
      '<ellipse cx="62" cy="26" rx="10.5" ry="13.5" fill="#fff" stroke="#1b1b1b" stroke-width="3"/>' +
      '<circle cx="40.5" cy="29" r="4" fill="#1b1b1b"/>' +
      '<circle cx="59.5" cy="29" r="4" fill="#1b1b1b"/>' +
      '</svg>' +
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
