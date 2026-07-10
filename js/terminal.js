/* Microsoft University — PowerShell terminal easter egg.
   Press ~ (backquote) to toggle. Esc closes. */
(function () {
  "use strict";
  var PROMPT = "PS MSFTU:\\> ";
  var box, out, input, open = false;

  function build() {
    box = document.createElement("div");
    box.id = "msftu-terminal";
    box.style.cssText =
      "position:fixed;top:0;left:0;right:0;height:55vh;z-index:99997;display:none;" +
      "background:#012456;color:#eee;font-family:Consolas,'Cascadia Code',Menlo,monospace;" +
      "font-size:14px;box-shadow:0 8px 32px rgba(0,0,0,.5);border-bottom:2px solid #0a3a7a;";
    box.innerHTML =
      '<div id="msftu-term-out" style="height:calc(100% - 40px);overflow-y:auto;padding:14px 16px;white-space:pre-wrap;word-break:break-word"></div>' +
      '<div style="display:flex;padding:8px 16px;border-top:1px solid rgba(255,255,255,.15)">' +
      '<span style="color:#ffe97f">' + PROMPT + "</span>" +
      '<input id="msftu-term-in" style="flex:1;background:none;border:none;outline:none;color:#fff;' +
      "font:inherit;margin-left:6px\" autocomplete=\"off\" spellcheck=\"false\">" +
      "</div>";
    document.body.appendChild(box);
    out = document.getElementById("msftu-term-out");
    input = document.getElementById("msftu-term-in");
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { run(input.value); input.value = ""; }
      if (e.key === "Escape") toggle(false);
      e.stopPropagation();
    });
    print("Microsoft University PowerShell (not really)\nCopyright (C) Alex de Jong. Type 'Get-Help' to begin, 'exit' to leave.\n", "#7fdbff");
  }

  function print(text, color) {
    var el = document.createElement("div");
    el.textContent = text;
    if (color) el.style.color = color;
    out.appendChild(el);
    out.scrollTop = out.scrollHeight;
  }

  function echo(cmd) { print(PROMPT + cmd, "#ffe97f"); }

  function upcoming() {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    return (typeof EVENTS !== "undefined" ? EVENTS : [])
      .filter(function (e) { return new Date(e.date + "T00:00:00") > t; })
      .sort(function (a, b) { return a.date < b.date ? -1 : 1; });
  }

  function run(raw) {
    var cmd = raw.trim();
    if (!cmd) return;
    echo(cmd);
    var c = cmd.toLowerCase();

    if (c === "get-help" || c === "help") {
      print(
        "Available cmdlets:\n" +
        "  Get-Alex          Who is this guy?\n" +
        "  Get-Events        Upcoming trainings & keynotes\n" +
        "  Book-Training     Opens the booking page\n" +
        "  Get-Whiteboards   The famous whiteboards\n" +
        "  Get-Resources     Learning resources\n" +
        "  Invoke-Keynote    Engage keynote mode\n" +
        "  Invoke-BSOD       You know what this does\n" +
        "  Get-Health        Service Health dashboard\n" +
        "  Get-Achievements  Your gamerscore & trophies\n" +
        "  Start-Break 15    Break screen for the projector (minutes...\n" +
        "  Start-Break 10:45 ...or an exact resume time)\n" +
        "  Enable-Aero       Windows Vista called...\n" +
        "  Disable-Aero      ...and 2026 answered\n" +
        "  cls / clear       Clear screen\n" +
        "  exit              Close terminal");
    } else if (c === "get-alex") {
      print(
        "Name              : Alex de Jong\nRole              : Speaker / Microsoft Evangelist / Trainer\n" +
        "BasedIn           : Netherlands\nYearsInEcosystem  : 20+\nCertifications    : Expert-level (Azure, Microsoft 365)\n" +
        "Specialties       : {AI, Security, Copilot, Storytelling}\nSlidesPerDemo     : 0.2\nCoffeeLevel       : Optimal");
    } else if (c === "get-events") {
      var evs = upcoming();
      if (!evs.length) { print("No upcoming events. Book-Training to change that."); return; }
      var lines = "Date        Title                                     City            Status\n" +
                  "----        -----                                     ----            ------\n";
      evs.forEach(function (e) {
        var status = e.soldout ? "SOLD OUT" : (e.url ? "Bookable" : "Enquire");
        lines += (e.date + "  " + pad(e.title, 40) + "  " + pad(e.city, 14) + "  " + status + "\n");
      });
      print(lines);
      print("Full list: events.html", "#7fdbff");
    } else if (c === "book-training") {
      print("Opening booking page...");
      setTimeout(function () { window.location.href = "contact.html"; }, 600);
    } else if (c === "get-whiteboards") {
      print("Opening whiteboards...");
      window.open("https://dejongms-my.sharepoint.com/:f:/g/personal/alex_alexdejong_com/EsVGJ2WLoU9Fowhg_7Czz9cBtJwC65C3fGvZNu5Yx0l31Q?e=evenrn", "_blank");
    } else if (c === "get-resources") {
      print("Opening learning resources...");
      setTimeout(function () { window.location.href = "resources.html"; }, 600);
    } else if (c === "invoke-keynote") {
      print("Starting keynote engine");
      var dots = 0, iv = setInterval(function () {
        print("Loading demo environment" + ".".repeat(++dots));
        if (dots >= 3) {
          clearInterval(iv);
          print("🎤 Keynote mode engaged. Expect demos, not slides.", "#7fff9f");
        }
      }, 350);
    } else if (c === "invoke-bsod") {
      if (window.__eggBsod) window.__eggBsod(); else print("BSOD module not loaded on this page.", "#f77");
    } else if (c === "enable-aero") {
      window.__setAero && window.__setAero(true);
      print("Aero glass enabled. Welcome to 2007. 🥂", "#7fdbff");
    } else if (c === "disable-aero") {
      window.__setAero && window.__setAero(false);
      print("Aero glass disabled. Welcome back.");
    } else if (c === "get-achievements") {
      var A = window.__achievements;
      if (!A) { print("Achievement module not loaded.", "#f77"); return; }
      var out2 = "Gamerscore: " + A.score() + "G / 1000G\n\n";
      A.defs.forEach(function (d) {
        out2 += (A.unlocked[d.id] ? "[x] " : "[ ] ") + pad(d.name, 26) + " " + pad(String(d.g) + "G", 5) + " " + d.desc + "\n";
      });
      print(out2);
    } else if (c.indexOf("start-break") === 0) {
      var arg = cmd.split(/\s+/).filter(Boolean)[1] || "15";
      var mins;
      var hm = arg.match(/^(\d{1,2})[:.](\d{2})$/);
      if (hm) {
        // absolute resume time, e.g. Start-Break 10:45 (rolls to tomorrow if past)
        var target = new Date();
        target.setHours(+hm[1], +hm[2], 0, 0);
        if (target <= new Date()) target.setDate(target.getDate() + 1);
        mins = (target - new Date()) / 60000;
        print("Break until " + arg + " — deploying scheduled maintenance window...");
      } else {
        mins = parseFloat(arg) || 15;
        print("Deploying scheduled maintenance window (" + mins + " min)...");
      }
      setTimeout(function () { startBreak(mins); }, 700);
    } else if (c === "stop-break") {
      window.__stopBreak("Break ended. Back to work.");
    } else if (c === "get-health" || c === "get-servicehealth") {
      print("Opening Service Health dashboard...");
      setTimeout(function () { window.location.href = "status.html"; }, 600);
    } else if (c === "cls" || c === "clear") {
      out.innerHTML = "";
    } else if (c === "exit") {
      toggle(false);
    } else {
      print(cmd.split(" ")[0] + " : The term '" + cmd.split(" ")[0] +
        "' is not recognized as the name of a cmdlet. Try Get-Help.", "#ff7b7b");
    }
  }

  function pad(s, n) { s = String(s); return s.length > n ? s.slice(0, n - 1) + "…" : s + " ".repeat(n - s.length); }

  function toggle(force) {
    open = typeof force === "boolean" ? force : !open;
    if (!box) build();
    box.style.display = open ? "block" : "none";
    if (open) { input.focus(); window.__achieve && window.__achieve("terminal"); }
  }

  document.addEventListener("keydown", function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    if ((e.key === "`" || e.key === "~") && tag !== "INPUT" && tag !== "TEXTAREA") {
      e.preventDefault();
      toggle();
    }
  });

  /* ---- Projector break screen (Start-Break) ---- */
  var breakEl = null, breakTimer = null;
  window.__stopBreak = function (msg) {
    if (breakTimer) { clearInterval(breakTimer); breakTimer = null; }
    if (breakEl) { breakEl.remove(); breakEl = null; }
    if (msg) print(msg);
  };
  function startBreak(minutes) {
    window.__stopBreak();
    var total = Math.max(1, Math.min(minutes || 15, 180)) * 60 * 1000;
    var endAt = Date.now() + total;
    var resume = new Date(endAt);
    var hh = ("0" + resume.getHours()).slice(-2), mm = ("0" + resume.getMinutes()).slice(-2);
    breakEl = document.createElement("div");
    breakEl.style.cssText =
      "position:fixed;inset:0;z-index:100000;background:#0067b8;color:#fff;" +
      "font-family:'Segoe UI Light','Segoe UI',sans-serif;display:flex;flex-direction:column;" +
      "align-items:center;justify-content:center;text-align:center;cursor:none";
    breakEl.innerHTML =
      '<div id="mu-break-spin" style="font-size:64px;animation:mu-spin 1.6s linear infinite">◌</div>' +
      '<div id="mu-break-pct" style="font-size:44px;font-weight:300;margin-top:36px">Working on updates 0% complete</div>' +
      '<div style="font-size:30px;font-weight:300;opacity:.85;margin-top:14px">Don\'t turn off your PC. Grab a coffee instead. ☕</div>' +
      '<div id="mu-break-count" style="font-size:96px;font-weight:200;margin-top:56px"></div>' +
      '<div style="font-size:28px;font-weight:300;opacity:.85;margin-top:10px">Class resumes at ' + hh + ":" + mm + '</div>' +
      '<div style="position:fixed;bottom:26px;font-size:18px;opacity:.5">Press Esc to end the break early (trainer only, obviously)</div>';
    var st = document.createElement("style");
    st.textContent = "@keyframes mu-spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}";
    breakEl.appendChild(st);
    document.body.appendChild(breakEl);
    toggle(false);
    breakTimer = setInterval(function () {
      var left = endAt - Date.now();
      if (left <= 0) {
        document.getElementById("mu-break-pct").textContent = "Updates complete. Welcome back!";
        document.getElementById("mu-break-count").textContent = "🎉";
        setTimeout(function () { window.__stopBreak(); }, 8000);
        clearInterval(breakTimer); breakTimer = null;
        return;
      }
      var pct = Math.min(99, Math.floor((1 - left / total) * 100));
      var m = Math.floor(left / 60000), s = Math.floor(left % 60000 / 1000);
      document.getElementById("mu-break-pct").textContent = "Working on updates " + pct + "% complete";
      document.getElementById("mu-break-count").textContent = m + ":" + ("0" + s).slice(-2);
    }, 250);
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && breakEl) window.__stopBreak();
  });

  /* ---- Windows Vista / Aero mode ---- */
  var aeroCssLoaded = false;
  window.__setAero = function (on) {
    if (on && !aeroCssLoaded) {
      var l = document.createElement("link");
      l.rel = "stylesheet"; l.href = "css/aero.css";
      document.head.appendChild(l);
      aeroCssLoaded = true;
    }
    document.body.classList.toggle("aero", on);
    if (on && window.__achieve) window.__achieve("aero");
    try { localStorage.setItem("msftu-aero", on ? "1" : "0"); } catch (e) {}
  };
  try {
    if (localStorage.getItem("msftu-aero") === "1") window.__setAero(true);
  } catch (e) {}
  // typing "vista" anywhere (outside inputs) toggles it
  var buf = "";
  document.addEventListener("keydown", function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA" || e.key.length !== 1) return;
    buf = (buf + e.key.toLowerCase()).slice(-5);
    if (buf === "vista") {
      window.__setAero(!document.body.classList.contains("aero"));
      buf = "";
    }
  });
})();
