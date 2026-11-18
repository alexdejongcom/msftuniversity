/* Release notes "what's new" — Learning Resources page.
 * Data: /api/whatsnew (server-side parse of the Microsoft Learn release-notes
 * pages for Microsoft 365 Copilot, Defender, Sentinel and Purview). Product chips filter the list.
 * Renders with textContent only — titles come from an external site. */
(function () {
  "use strict";
  var list = document.getElementById("whatsnew-list");
  var chips = document.getElementById("whatsnew-chips");
  if (!list || !chips) return;
  var card = document.getElementById("whatsnew-card");
  var section = document.getElementById("news-section");

  // source → [short chip label, colour]
  var PRODUCTS = {
    "Microsoft 365 Copilot":   ["Copilot", "#8661c5"],
    "Defender for Office 365": ["Office 365", "#c43e1c"],
    "Defender for Endpoint":   ["Endpoint", "#0f6cbd"],
    "Defender for Identity":   ["Identity", "#5c2d91"],
    "Defender for Cloud Apps": ["Cloud Apps", "#008575"],
    "Defender for Cloud":      ["Cloud", "#0078d4"],
    "Microsoft Sentinel":      ["Sentinel", "#004e8c"],
    "Microsoft Purview":       ["Purview", "#0b7a75"],
  };
  var ALL_LIMIT = 12;
  var items = [], current = "all";

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function render() {
    var rows = current === "all"
      ? items.slice(0, ALL_LIMIT)
      : items.filter(function (it) { return it.source === current; });
    list.innerHTML = "";
    rows.forEach(function (it) {
      var p = PRODUCTS[it.source] || [it.source, "#5c5c5c"];
      var li = document.createElement("li");
      var a = el("a");
      a.href = it.link; a.target = "_blank"; a.rel = "noopener";
      a.title = it.source + " — " + it.title;
      var main = el("span", "wn-main");
      var src = el("span", "wn-src", /^Defender/.test(it.source) ? "Defender \u00B7 " + p[0] : p[0]);
      src.style.background = p[1];
      main.appendChild(src);
      main.appendChild(el("span", null, it.title));
      if (it.stage) main.appendChild(el("span", "wn-stage " + it.stage, it.stage === "GA" ? "GA" : it.stage));
      a.appendChild(main);
      a.appendChild(el("span", "desc wn-when", it.month));
      li.appendChild(a);
      list.appendChild(li);
    });
    var foot = card.querySelector(".wn-foot");
    if (!foot) { foot = el("p", "wn-foot"); card.appendChild(foot); }
    foot.textContent = current === "all"
      ? "Showing the " + rows.length + " most recent changes across all products. Source: Microsoft Learn."
      : "Latest changes for " + current + ". Source: Microsoft Learn.";
  }

  function chip(key, label, color) {
    var b = el("button", "wn-chip");
    b.type = "button";
    b.setAttribute("aria-pressed", key === current ? "true" : "false");
    if (color) { var d = el("span", "dot"); d.style.background = color; b.appendChild(d); }
    b.appendChild(document.createTextNode(label));
    if (key !== "all") b.title = key;
    b.addEventListener("click", function () {
      current = key;
      Array.prototype.forEach.call(chips.children, function (c) { c.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      render();
    });
    chips.appendChild(b);
  }

  fetch("/api/whatsnew")
    .then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); })
    .then(function (data) {
      if (!data || !data.length) throw new Error("empty");
      items = data;
      chip("all", "All products");
      Object.keys(PRODUCTS).forEach(function (src) {
        var label = /^Defender/.test(src) ? src : src === "Microsoft 365 Copilot" ? "Microsoft 365 Copilot" : src.replace(/^Microsoft /, "");
        if (items.some(function (it) { return it.source === src; })) chip(src, label, PRODUCTS[src][1]);
      });
      render();
    })
    .catch(function () {
      if (card) card.style.display = "none";
      var alive = ["whatsnew-card", "roadmap-card", "news-card"].some(function (id) {
        var c = document.getElementById(id); return c && c.style.display !== "none";
      });
      if (section && !alive) section.style.display = "none";
    });
})();
