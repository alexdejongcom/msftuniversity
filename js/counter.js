/* Visitor counter widget — retro odometer, powered by /api/counter
 * (Azure Functions + Table Storage — yes, really, ask Alex about it).
 * Counts once per browser session; other page views just display.
 * Hides itself silently if the API isn't reachable (e.g. local preview). */
(function () {
  "use strict";
  var footer = document.querySelector(".footer-bottom");
  if (!footer) return;

  var counted = false;
  try { counted = sessionStorage.getItem("msftu-counted") === "1"; } catch (e) {}

  fetch("/api/counter", { method: counted ? "GET" : "POST" })
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (data) {
      if (typeof data.count !== "number") return;
      try { sessionStorage.setItem("msftu-counted", "1"); } catch (e) {}
      render(data.count);
    })
    .catch(function () { /* no API, no counter — stay classy */ });

  function render(count) {
    var digits = String(count).padStart(6, "0").split("");
    var box = document.createElement("span");
    box.title = "Live from an Azure Function + Table Storage. Ask us how.";
    box.style.cssText = "display:inline-flex;align-items:center;gap:6px";
    var label = document.createElement("span");
    label.textContent = "You are visitor";
    box.appendChild(label);
    var odo = document.createElement("span");
    odo.style.cssText = "display:inline-flex;gap:2px";
    digits.forEach(function (d) {
      var cell = document.createElement("span");
      cell.textContent = d;
      cell.style.cssText =
        "background:#171717;color:#7fba00;font-family:Consolas,monospace;font-weight:700;" +
        "padding:1px 5px;border-radius:3px;font-size:12px;border:1px solid #444";
      odo.appendChild(cell);
    });
    box.appendChild(odo);
    footer.appendChild(box);
  }
})();
