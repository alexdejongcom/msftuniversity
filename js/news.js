/* Latest Microsoft news — Learning Resources page.
 * Pulls merged official Microsoft blog posts from /api/news (server-side
 * RSS proxy, 15-min cache). Renders with textContent only — feed titles
 * are external content and must never hit innerHTML. */
(function () {
  "use strict";
  var list = document.getElementById("news-list");
  if (!list) return;
  var section = document.getElementById("news-section");

  var BADGE = {
    "Official Microsoft Blog": "#0067b8",
    "Microsoft 365": "#d83b01",
    "Azure": "#008575",
  };

  function ago(iso) {
    var s = (Date.now() - new Date(iso).getTime()) / 1000;
    if (s < 3600) return Math.max(1, Math.round(s / 60)) + " min ago";
    if (s < 86400) return Math.round(s / 3600) + " h ago";
    var d = Math.round(s / 86400);
    return d === 1 ? "yesterday" : d + " days ago";
  }

  fetch("/api/news")
    .then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); })
    .then(function (items) {
      if (!items || !items.length) throw new Error("empty");
      list.innerHTML = "";
      items.forEach(function (it) {
        var li = document.createElement("li");

        var badge = document.createElement("span");
        badge.textContent = it.source;
        badge.style.cssText =
          "display:inline-block;font-size:11.5px;font-weight:600;color:#fff;padding:2px 9px;" +
          "border-radius:10px;margin-right:10px;white-space:nowrap;vertical-align:2px;background:" +
          (BADGE[it.source] || "#5c5c5c");

        var a = document.createElement("a");
        a.href = it.link;
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = it.title;

        var when = document.createElement("span");
        when.className = "desc";
        when.textContent = ago(it.date);

        li.appendChild(badge);
        li.appendChild(a);
        li.appendChild(document.createTextNode(" "));
        li.appendChild(when);
        list.appendChild(li);
      });
    })
    .catch(function () {
      // No news is bad news — hide the section rather than show an error.
      if (section) section.style.display = "none";
    });
})();
