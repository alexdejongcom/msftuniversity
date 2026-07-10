/* Certificate of Attendance — generated for the course that is currently
 * running (grace period: up to 3 days after it ends). Data comes from
 * js/events.js. Rendered on canvas at print-friendly resolution. */
(function () {
  "use strict";
  var btn = document.getElementById("cert-generate");
  if (!btn) return;
  var nameInput = document.getElementById("cert-name");
  var result = document.getElementById("cert-result");
  var section = document.getElementById("cert-form");
  var notice = document.getElementById("cert-notice");

  var GRACE_DAYS = 3;
  var MONTHS = ["January","February","March","April","May","June","July",
                "August","September","October","November","December"];

  function fmt(iso) {
    var d = new Date(iso + "T00:00:00");
    return d.getDate() + " " + MONTHS[d.getMonth()] + " " + d.getFullYear();
  }

  function runningEvent() {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    var evs = (typeof EVENTS !== "undefined" ? EVENTS : []);
    for (var i = 0; i < evs.length; i++) {
      var e = evs[i];
      var start = new Date(e.date + "T00:00:00");
      var end = new Date((e.end || e.date) + "T00:00:00");
      var graceEnd = new Date(end); graceEnd.setDate(graceEnd.getDate() + GRACE_DAYS);
      if (start <= t && t <= graceEnd) return e;
    }
    return null;
  }

  var ev = runningEvent();
  if (!ev) {
    if (section) section.style.display = "none";
    if (notice) notice.style.display = "block";
    return;
  }

  // deterministic verification code from name + course date
  function verifyCode(name, date) {
    var s = (name.toLowerCase().trim() + "|" + date);
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = (h * 16777619) >>> 0;
    }
    return ("00000000" + h.toString(16).toUpperCase()).slice(-8);
  }

  btn.addEventListener("click", function () {
    var name = (nameInput.value || "").trim();
    if (!name) { nameInput.focus(); return; }
    window.__achieve && window.__achieve("cert");

    var W = 2200, H = 1556;
    var c = document.createElement("canvas");
    c.width = W; c.height = H;
    var x = c.getContext("2d");
    var SEGOE = "'Segoe UI', 'Selawik', 'Helvetica Neue', sans-serif";
    var M = 170; // left margin — Microsoft's flat, left-aligned layout

    // clean white sheet
    x.fillStyle = "#ffffff"; x.fillRect(0, 0, W, H);

    // giant four-square watermark, bottom-right, barely-there
    (function () {
      var s = 340, g = 28, wx = W - 2 * s - g - 120, wy = H - 2 * s - g - 120;
      x.globalAlpha = 0.05;
      x.fillStyle = "#f25022"; x.fillRect(wx, wy, s, s);
      x.fillStyle = "#7fba00"; x.fillRect(wx + s + g, wy, s, s);
      x.fillStyle = "#00a4ef"; x.fillRect(wx, wy + s + g, s, s);
      x.fillStyle = "#ffb900"; x.fillRect(wx + s + g, wy + s + g, s, s);
      x.globalAlpha = 1;
    })();

    // brand lockup, top-left: four squares + wordmark (like the MS logo)
    var sq = 52, gap = 9, by = 130;
    x.fillStyle = "#f25022"; x.fillRect(M, by, sq, sq);
    x.fillStyle = "#7fba00"; x.fillRect(M + sq + gap, by, sq, sq);
    x.fillStyle = "#00a4ef"; x.fillRect(M, by + sq + gap, sq, sq);
    x.fillStyle = "#ffb900"; x.fillRect(M + sq + gap, by + sq + gap, sq, sq);
    x.textAlign = "left";
    x.fillStyle = "#737373";
    x.font = "400 64px " + SEGOE;
    x.fillText("Microsoft University", M + 2 * sq + gap + 40, by + sq + gap + 14);

    // heading — Segoe UI Light, the Microsoft certificate voice
    x.fillStyle = "#1b1b1b";
    x.font = "200 128px " + SEGOE;
    x.fillText("Certificate of Attendance", M, 480);

    // Microsoft-blue accent rule
    x.fillStyle = "#0067b8";
    x.fillRect(M, 530, 220, 8);

    x.fillStyle = "#737373";
    x.font = "400 42px " + SEGOE;
    x.fillText("This certificate is presented to", M, 660);

    // attendee name — big, semibold, flat (no script fonts in Fluent)
    x.fillStyle = "#0067b8";
    x.font = "600 118px " + SEGOE;
    x.fillText(name, M, 800);

    x.fillStyle = "#737373";
    x.font = "400 42px " + SEGOE;
    x.fillText("for attending", M, 900);

    x.fillStyle = "#1b1b1b";
    x.font = "600 68px " + SEGOE;
    wrapLeft(x, ev.title, M, 985, W - M - 420, 82);

    var range = fmt(ev.date) + (ev.end && ev.end !== ev.date ? " – " + fmt(ev.end) : "");
    x.fillStyle = "#454545";
    x.font = "400 42px " + SEGOE;
    x.fillText(range + "   ·   " + ev.city, M, 1130);

    // baseline rule above the footer row
    x.strokeStyle = "#e1e1e1"; x.lineWidth = 2;
    x.beginPath(); x.moveTo(M, 1240); x.lineTo(W - M, 1240); x.stroke();

    // footer row — signature left, verification right
    x.fillStyle = "#1b1b1b";
    x.font = "italic 58px 'Segoe Script', 'Brush Script MT', cursive";
    x.fillText("Alex de Jong", M, 1330);
    x.fillStyle = "#737373";
    x.font = "400 30px " + SEGOE;
    x.fillText("Alex de Jong · Microsoft Certified Trainer", M, 1382);

    var code = "MU-" + ev.date.replace(/-/g, "") + "-" + verifyCode(name, ev.date);
    x.textAlign = "right";
    x.fillStyle = "#1b1b1b";
    x.font = "600 32px Consolas, monospace";
    x.fillText("Certificate ID: " + code, W - M, 1330);
    x.fillStyle = "#737373";
    x.font = "400 30px " + SEGOE;
    x.fillText("Issued " + fmt(new Date().toISOString().slice(0, 10)) + " · msftuniversity.com", W - M, 1382);

    // honesty footer
    x.textAlign = "center";
    x.fillStyle = "#9a9a9a";
    x.font = "400 24px " + SEGOE;
    x.fillText("Issued by Microsoft University (Alex de Jong), an independent training practice. " +
               "This document confirms attendance and is not a Microsoft Corporation certification.", W / 2, 1480);
    x.textAlign = "left";

    // register the certificate (fire-and-forget; generation works regardless)
    try {
      fetch("/api/certificate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, code: code, course: ev.title, date: ev.date }),
      }).catch(function () {});
    } catch (e) {}

    var url = c.toDataURL("image/png");
    result.innerHTML =
      '<img src="' + url + '" alt="Certificate of attendance" style="width:100%;max-width:860px;border:1px solid var(--border);border-radius:8px;box-shadow:var(--shadow-md)">' +
      '<p style="margin-top:14px"><a class="btn btn-blue" download="certificate-of-attendance.png" href="' + url + '">Download certificate</a>' +
      ' <span style="font-size:13.5px;color:var(--ink-faint);margin-left:10px">Tip: print to PDF for a crisp A4 copy.</span></p>';
  });

  function wrapLeft(ctx, text, lx, y, maxW, lineH) {
    var words = text.split(" "), line = "", lines = [];
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = w; }
      else line = test;
    });
    lines.push(line);
    lines.forEach(function (l, i) { ctx.fillText(l, lx, y + i * lineH); });
  }
})();
