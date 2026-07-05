/* Boarding pass generator — personalizes a "Microsoft University Air"
   boarding pass for the course currently running (or up next). */
(function () {
  "use strict";
  var btn = document.getElementById("bp-generate");
  if (!btn) return;
  var nameInput = document.getElementById("bp-name");
  var result = document.getElementById("bp-result");

  function currentEvent() {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    var evs = (typeof EVENTS !== "undefined" ? EVENTS : [])
      .slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; });
    var cur = null, next = null;
    evs.forEach(function (e) {
      var s = new Date(e.date + "T00:00:00"), en = new Date((e.end || e.date) + "T00:00:00");
      if (!cur && s <= t && t <= en) cur = e;
      if (!next && s > t) next = e;
    });
    return cur || next;
  }

  btn.addEventListener("click", function () {
    var name = (nameInput.value || "").trim();
    if (!name) { nameInput.focus(); nameInput.placeholder = "Your name first! ✈️"; return; }
    var ev = currentEvent();
    var c = document.createElement("canvas");
    c.width = 1200; c.height = 420;
    var x = c.getContext("2d");

    // body
    x.fillStyle = "#ffffff"; x.fillRect(0, 0, 1200, 420);
    // header band
    var grad = x.createLinearGradient(0, 0, 1200, 0);
    grad.addColorStop(0, "#003d6b"); grad.addColorStop(1, "#0a8ee0");
    x.fillStyle = grad; x.fillRect(0, 0, 1200, 86);
    // four squares
    [["#f25022", 30, 22], ["#7fba00", 55, 22], ["#00a4ef", 30, 47], ["#ffb900", 55, 47]].forEach(function (sq) {
      x.fillStyle = sq[0]; x.fillRect(sq[1], sq[2], 21, 21);
    });
    x.fillStyle = "#fff";
    x.font = "700 30px 'Segoe UI', sans-serif";
    x.fillText("MICROSOFT UNIVERSITY AIR", 95, 55);
    x.font = "600 20px 'Segoe UI', sans-serif";
    x.textAlign = "right";
    x.fillText("BOARDING PASS", 1160, 55);
    x.textAlign = "left";

    // stub separator
    x.strokeStyle = "#c9c9c9"; x.setLineDash([8, 8]);
    x.beginPath(); x.moveTo(880, 86); x.lineTo(880, 420); x.stroke();
    x.setLineDash([]);

    function field(label, value, fx, fy, big) {
      x.fillStyle = "#767676"; x.font = "600 15px 'Segoe UI', sans-serif";
      x.fillText(label, fx, fy);
      x.fillStyle = "#171717"; x.font = (big ? "700 30px" : "600 23px") + " 'Segoe UI', sans-serif";
      x.fillText(value, fx, fy + (big ? 36 : 30));
    }

    var city = ev ? ev.city.split(",")[0].toUpperCase() : "THE CLOUD";
    var date = ev ? ev.date : new Date().toISOString().slice(0, 10);
    var flight = "MU-" + date.replace(/-/g, "").slice(4);
    var seat = (1 + Math.floor(Math.random() * 30)) + "ABCDEF"[Math.floor(Math.random() * 6)];

    field("PASSENGER", name.toUpperCase().slice(0, 26), 40, 130, true);
    field("FROM", "CURIOSITY", 40, 220);
    field("TO", "CERTIFICATION", 300, 220);
    field("VIA", city, 620, 220);
    field("FLIGHT", flight, 40, 310);
    field("DATE", date, 300, 310);
    field("GATE", "C4", 620, 310);
    field("SEAT", seat, 760, 310);
    x.fillStyle = "#0067b8"; x.font = "italic 600 17px 'Segoe UI', sans-serif";
    x.fillText(ev ? "Now boarding: " + ev.title : "Now boarding: your Microsoft journey", 40, 385);

    // stub
    field("PASSENGER", name.toUpperCase().slice(0, 14), 910, 130);
    field("FLIGHT", flight, 910, 220);
    field("SEAT", seat, 1080, 220);
    // barcode
    var bx = 910;
    while (bx < 1160) {
      var w = 2 + Math.floor(Math.random() * 5);
      if (Math.random() > 0.4) { x.fillStyle = "#171717"; x.fillRect(bx, 280, w, 100); }
      bx += w + 2;
    }

    var url = c.toDataURL("image/png");
    result.innerHTML =
      '<img src="' + url + '" alt="Your boarding pass" style="width:100%;max-width:760px;border:1px solid var(--border);border-radius:8px;box-shadow:var(--shadow-md)">' +
      '<p style="margin-top:12px"><a class="btn btn-blue" download="microsoft-university-boarding-pass.png" href="' + url + '">Download boarding pass</a>' +
      ' <span style="font-size:13.5px;color:var(--ink-faint);margin-left:10px">Post it on LinkedIn and tag me ✈️</span></p>';
  });
})();
