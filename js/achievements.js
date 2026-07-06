/* Microsoft University — Xbox-style achievement system.
   Explore the site, unlock achievements, collect 1000G.
   Progress persists in localStorage. Other scripts report unlocks
   via window.__achieve("id"). */
(function () {
  "use strict";

  var DEFS = [
    { id: "hello",    name: "Hello, World",            desc: "Visit Microsoft University",                       g: 50  },
    { id: "tourist",  name: "Grand Tour",              desc: "Visit every main page of the site",                g: 100 },
    { id: "terms",    name: "Fine Print Enthusiast",   desc: "Actually read the Terms & Conditions",             g: 50  },
    { id: "status",   name: "Site Reliability Engineer", desc: "Check the Service Health dashboard",             g: 50  },
    { id: "terminal", name: "PowerShell to the People", desc: "Open the hidden terminal (~)",                    g: 100 },
    { id: "bsod",     name: "Blue Screen of Success",  desc: "Trigger the BSOD. You know how.",                  g: 100 },
    { id: "clippy",   name: "It Looks Like…",          desc: "Summon Clippy from his eternal slumber",           g: 100 },
    { id: "aero",     name: "Glass Half Full",         desc: "Enable Windows Vista mode",                        g: 100 },
    { id: "globe",    name: "Spin Doctor",             desc: "Give the tour globe a spin",                       g: 50  },
    { id: "cert",     name: "Certified Awesome",       desc: "Generate a certificate of attendance",             g: 100 },
    { id: "all",      name: "Completionist",           desc: "Unlock every other achievement",                   g: 200 }
  ];
  var PAGES = ["index.html", "course-today.html", "events.html", "training.html",
               "resources.html", "about.html", "contact.html"];
  var KEY = "msftu-ach", PKEY = "msftu-ach-pages";

  function load(k) {
    try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; }
  }
  function save(k, v) {
    try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {}
  }
  var unlocked = load(KEY);

  function def(id) { for (var i = 0; i < DEFS.length; i++) if (DEFS[i].id === id) return DEFS[i]; }
  function score() {
    var s = 0; DEFS.forEach(function (d) { if (unlocked[d.id]) s += d.g; }); return s;
  }

  /* ---- toast queue (Xbox style) ---- */
  var queue = [], showing = false;
  function toast(d) {
    queue.push(d);
    if (!showing) next();
  }
  function next() {
    var d = queue.shift();
    if (!d) { showing = false; return; }
    showing = true;
    var el = document.createElement("div");
    el.style.cssText =
      "position:fixed;left:50%;bottom:28px;transform:translate(-50%,120px);z-index:99996;" +
      "display:flex;align-items:center;gap:14px;background:#1f1f1f;color:#fff;border-radius:40px;" +
      "padding:10px 26px 10px 12px;box-shadow:0 12px 40px rgba(0,0,0,.45);cursor:pointer;" +
      "font-family:'Segoe UI',sans-serif;transition:transform .45s cubic-bezier(.2,.9,.3,1.2);max-width:92vw";
    el.innerHTML =
      '<span style="width:44px;height:44px;border-radius:50%;background:#107c10;display:flex;' +
      'align-items:center;justify-content:center;font-size:22px;flex:none">🏆</span>' +
      '<span style="min-width:0"><span style="display:block;font-size:12px;color:#9d9d9d">Achievement unlocked · ' + d.g + 'G</span>' +
      '<span style="display:block;font-size:15.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + d.name + "</span></span>";
    el.addEventListener("click", function () { el.remove(); panel(); });
    document.body.appendChild(el);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.style.transform = "translate(-50%,0)"; });
    });
    chime();
    setTimeout(function () {
      el.style.transform = "translate(-50%,120px)";
      setTimeout(function () { el.remove(); next(); }, 500);
    }, 4200);
  }

  function chime() {
    try {
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return;
      var ctx = chime.ctx || (chime.ctx = new C());
      if (ctx.state === "suspended") return;
      [523.25, 783.99].forEach(function (f, i) {
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.frequency.value = f; o.type = "sine";
        g.gain.setValueAtTime(0.0001, ctx.currentTime + i * 0.09);
        g.gain.exponentialRampToValueAtTime(0.12, ctx.currentTime + i * 0.09 + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.09 + 0.5);
        o.connect(g); g.connect(ctx.destination);
        o.start(ctx.currentTime + i * 0.09); o.stop(ctx.currentTime + i * 0.09 + 0.55);
      });
    } catch (e) {}
  }

  /* ---- achievements panel ---- */
  function panel() {
    if (document.getElementById("msftu-ach-panel")) return;
    var wrap = document.createElement("div");
    wrap.id = "msftu-ach-panel";
    wrap.style.cssText =
      "position:fixed;inset:0;z-index:99995;background:rgba(0,0,0,.55);display:flex;" +
      "align-items:center;justify-content:center;padding:20px;font-family:'Segoe UI',sans-serif";
    var rows = DEFS.map(function (d) {
      var got = !!unlocked[d.id];
      return '<div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid #333;opacity:' + (got ? 1 : 0.5) + '">' +
        '<span style="width:38px;height:38px;border-radius:50%;background:' + (got ? "#107c10" : "#3a3a3a") +
        ';display:flex;align-items:center;justify-content:center;font-size:18px;flex:none">' + (got ? "🏆" : "🔒") + "</span>" +
        '<span style="flex:1;min-width:0"><b style="font-size:14.5px">' + d.name + "</b>" +
        '<span style="display:block;font-size:12.5px;color:#9d9d9d">' + d.desc + "</span></span>" +
        '<span style="font-size:13px;color:' + (got ? "#7fdb7f" : "#777") + ';flex:none">' + d.g + "G</span></div>";
    }).join("");
    wrap.innerHTML =
      '<div style="background:#1f1f1f;color:#fff;border-radius:12px;max-width:520px;width:100%;max-height:84vh;overflow-y:auto;padding:26px 28px">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">' +
      '<h2 style="font-size:19px;margin:0">Achievements</h2>' +
      '<button id="msftu-ach-close" style="background:none;border:none;color:#9d9d9d;font-size:22px;cursor:pointer;line-height:1">×</button></div>' +
      '<p style="font-size:13px;color:#9d9d9d;margin:0 0 14px">Gamerscore: <b style="color:#7fdb7f">' + score() + 'G</b> / 1000G — keep exploring the site to unlock the rest.</p>' +
      rows + "</div>";
    wrap.addEventListener("click", function (e) { if (e.target === wrap) wrap.remove(); });
    document.body.appendChild(wrap);
    document.getElementById("msftu-ach-close").addEventListener("click", function () { wrap.remove(); });
  }

  /* ---- unlock logic ---- */
  function achieve(id) {
    var d = def(id);
    if (!d || unlocked[id]) return;
    unlocked[id] = Date.now();
    save(KEY, unlocked);
    toast(d);
    if (id !== "all" && DEFS.every(function (x) { return x.id === "all" || unlocked[x.id]; })) {
      setTimeout(function () { achieve("all"); }, 600);
    }
  }
  window.__achieve = achieve;
  window.__achievements = { defs: DEFS, unlocked: unlocked, score: score, panel: panel };

  /* ---- page-visit achievements ---- */
  var page = (location.pathname.split("/").pop() || "index.html");
  achieve("hello");
  if (page === "terms.html") achieve("terms");
  if (page === "status.html") achieve("status");
  if (PAGES.indexOf(page) !== -1) {
    var seen = load(PKEY);
    seen[page] = 1;
    save(PKEY, seen);
    if (PAGES.every(function (p) { return seen[p]; })) achieve("tourist");
  }
})();
