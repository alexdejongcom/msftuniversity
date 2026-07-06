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

    // background + double border
    x.fillStyle = "#ffffff"; x.fillRect(0, 0, W, H);
    x.strokeStyle = "#003d6b"; x.lineWidth = 10;
    x.strokeRect(70, 70, W - 140, H - 140);
    x.strokeStyle = "#0067b8"; x.lineWidth = 2;
    x.strokeRect(95, 95, W - 190, H - 190);

    // four-square mark, centered top
    var sq = 34, gap = 6, bx = W / 2 - sq - gap / 2, by = 175;
    x.fillStyle = "#f25022"; x.fillRect(bx, by, sq, sq);
    x.fillStyle = "#7fba00"; x.fillRect(bx + sq + gap, by, sq, sq);
    x.fillStyle = "#00a4ef"; x.fillRect(bx, by + sq + gap, sq, sq);
    x.fillStyle = "#ffb900"; x.fillRect(bx + sq + gap, by + sq + gap, sq, sq);

    x.textAlign = "center";
    x.fillStyle = "#737373";
    x.font = "600 34px 'Segoe UI', sans-serif";
    x.fillText("M I C R O S O F T   U N I V E R S I T Y", W / 2, 305);
    x.fillStyle = "#003d6b";
    x.font = "700 96px 'Segoe UI', Georgia, serif";
    x.fillText("Certificate of Attendance", W / 2, 430);

    x.fillStyle = "#454545";
    x.font = "400 40px 'Segoe UI', sans-serif";
    x.fillText("This is to certify that", W / 2, 560);

    // attendee name
    x.fillStyle = "#171717";
    x.font = "italic 700 110px Georgia, 'Times New Roman', serif";
    x.fillText(name, W / 2, 710);
    var nw = Math.min(x.measureText(name).width + 80, W - 500);
    x.strokeStyle = "#0067b8"; x.lineWidth = 3;
    x.beginPath(); x.moveTo(W / 2 - nw / 2, 745); x.lineTo(W / 2 + nw / 2, 745); x.stroke();

    x.fillStyle = "#454545";
    x.font = "400 40px 'Segoe UI', sans-serif";
    x.fillText("has attended the course", W / 2, 840);

    x.fillStyle = "#003d6b";
    x.font = "700 62px 'Segoe UI', sans-serif";
    wrap(x, ev.title, W / 2, 930, W - 500, 74);

    var range = fmt(ev.date) + (ev.end && ev.end !== ev.date ? " – " + fmt(ev.end) : "");
    var loc = ev.city + (ev.venue ? " · " + ev.venue : "");
    x.fillStyle = "#454545";
    x.font = "400 40px 'Segoe UI', sans-serif";
    x.fillText(range, W / 2, 1075);
    x.fillText(loc, W / 2, 1135);

    // signature block (left)
    x.textAlign = "left";
    x.fillStyle = "#171717";
    x.font = "italic 64px 'Segoe Script', 'Brush Script MT', cursive";
    x.fillText("Alex de Jong", 240, 1300);
    x.strokeStyle = "#454545"; x.lineWidth = 2;
    x.beginPath(); x.moveTo(230, 1330); x.lineTo(700, 1330); x.stroke();
    x.fillStyle = "#454545";
    x.font = "400 30px 'Segoe UI', sans-serif";
    x.fillText("Alex de Jong — Microsoft Certified Trainer", 230, 1375);

    // verification block (right)
    var code = "MU-" + ev.date.replace(/-/g, "") + "-" + verifyCode(name, ev.date);
    x.textAlign = "right";
    x.fillStyle = "#454545";
    x.font = "600 30px Consolas, monospace";
    x.fillText(code, W - 230, 1300);
    x.font = "400 28px 'Segoe UI', sans-serif";
    x.fillText("Issued " + fmt(new Date().toISOString().slice(0, 10)), W - 230, 1345);
    x.fillText("microsoftuniversity.com", W - 230, 1385);

    // honesty footer
    x.textAlign = "center";
    x.fillStyle = "#9a9a9a";
    x.font = "400 24px 'Segoe UI', sans-serif";
    x.fillText("Issued by Microsoft University (Alex de Jong), an independent training practice. " +
               "This document confirms attendance and is not a Microsoft Corporation certification.", W / 2, 1445);

    var url = c.toDataURL("image/png");
    result.innerHTML =
      '<img src="' + url + '" alt="Certificate of attendance" style="width:100%;max-width:860px;border:1px solid var(--border);border-radius:8px;box-shadow:var(--shadow-md)">' +
      '<p style="margin-top:14px"><a class="btn btn-blue" download="certificate-of-attendance.png" href="' + url + '">Download certificate</a>' +
      ' <span style="font-size:13.5px;color:var(--ink-faint);margin-left:10px">Tip: print to PDF for a crisp A4 copy.</span></p>';
  });

  function wrap(ctx, text, cx, y, maxW, lineH) {
    var words = text.split(" "), line = "", lines = [];
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = w; }
      else line = test;
    });
    lines.push(line);
    lines.forEach(function (l, i) { ctx.fillText(l, cx, y + i * lineH); });
  }
})();
