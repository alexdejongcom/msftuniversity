/* Microsoft 365 roadmap — Learning Resources page.
 * Data: /api/roadmap (newest entries from the public Microsoft 365 roadmap).
 * Status chips filter the list. textContent only — titles are external. */
(function () {
  "use strict";
  var list = document.getElementById("roadmap-list");
  var chips = document.getElementById("roadmap-chips");
  if (!list || !chips) return;
  var card = document.getElementById("roadmap-card");
  var section = document.getElementById("news-section");

  var STATUS = { "In development": "#8a6100", "Rolling out": "#0f6cbd", "Launched": "#0e700e" };
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var LIMIT = 12;
  var items = [], current = "all";

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function short(product) {
    return String(product || "")
      .replace(/^Microsoft Copilot \(Microsoft 365\)$/, "Copilot")
      .replace(/^Microsoft 365 /, "")
      .replace(/^Microsoft /, "");
  }
  function ga(s) {
    var m = /^(\d{4})-(\d{2})$/.exec(s || "");
    return m ? "GA " + MON[+m[2] - 1] + " " + m[1] : "";
  }

  function render() {
    var rows = items.filter(function (it) { return current === "all" || it.status === current; }).slice(0, LIMIT);
    list.innerHTML = "";
    if (!rows.length) { list.appendChild(el("li", null)).appendChild(el("span", "desc", "Nothing new with this status right now.")); return; }
    rows.forEach(function (it) {
      var li = document.createElement("li");
      var a = el("a");
      a.href = it.link; a.target = "_blank"; a.rel = "noopener";
      a.title = it.product + " — " + it.title;
      var main = el("span", "wn-main");
      var src = el("span", "wn-src", short(it.product));
      src.style.background = "#3b4a5c";
      main.appendChild(src);
      main.appendChild(el("span", null, it.title));
      if (it.status) {
        var st = el("span", "wn-stage", it.status);
        st.style.cssText = "background:#f3f2f1;color:" + (STATUS[it.status] || "#555");
        main.appendChild(st);
      }
      a.appendChild(main);
      a.appendChild(el("span", "desc wn-when", ga(it.ga)));
      li.appendChild(a);
      list.appendChild(li);
    });
  }

  function chip(key, label, color) {
    var b = el("button", "wn-chip");
    b.type = "button";
    b.setAttribute("aria-pressed", key === current ? "true" : "false");
    if (color) { var d = el("span", "dot"); d.style.background = color; b.appendChild(d); }
    b.appendChild(document.createTextNode(label));
    b.addEventListener("click", function () {
      current = key;
      Array.prototype.forEach.call(chips.children, function (c) { c.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      render();
    });
    chips.appendChild(b);
  }

  fetch("/api/roadmap")
    .then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); })
    .then(function (data) {
      if (!data || !data.length) throw new Error("empty");
      items = data;
      chip("all", "Everything new");
      Object.keys(STATUS).forEach(function (s) {
        if (items.some(function (it) { return it.status === s; })) chip(s, s, STATUS[s]);
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
