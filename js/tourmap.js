/* Tour map — plots upcoming events from js/events.js on a world map
   (countries fetched client-side from a public GeoJSON CDN) and flies
   a little plane along the route. Degrades gracefully if fetch fails. */
(function () {
  "use strict";
  var canvas = document.getElementById("tour-map");
  if (!canvas) return;
  var wrap = document.getElementById("tour-map-section");

  var COORDS = {
    "london":  [-0.12, 51.51],
    "redmond": [-122.12, 47.67],
    "oslo":    [10.75, 59.91],
    "gjøvik":  [10.69, 60.79],
    "gjovik":  [10.69, 60.79],
    "orlando": [-81.38, 28.54],
    "amsterdam": [4.90, 52.37],
    "anaheim": [-117.91, 33.84],
    "san diego": [-117.16, 32.72],
    "las vegas": [-115.14, 36.17]
  };

  function lookup(city) {
    if (!city) return null;
    var key = city.toLowerCase().split(",")[0].trim();
    return COORDS[key] || null;
  }

  var t = new Date(); t.setHours(0, 0, 0, 0);
  var stops = (typeof EVENTS !== "undefined" ? EVENTS : [])
    .filter(function (e) { return new Date((e.end || e.date) + "T00:00:00") >= t; })
    .sort(function (a, b) { return a.date < b.date ? -1 : 1; })
    .map(function (e) { return { e: e, ll: lookup(e.city) }; })
    .filter(function (s) { return s.ll; });

  if (stops.length < 2) { if (wrap) wrap.style.display = "none"; return; }

  var W = 1100, H = 520;
  canvas.width = W; canvas.height = H;
  var ctx = canvas.getContext("2d");
  // equirectangular projection, cropped to 75N..-55S for a nicer frame
  var LAT_TOP = 78, LAT_BOT = -56;
  function proj(ll) {
    var x = (ll[0] + 180) / 360 * W;
    var y = (LAT_TOP - ll[1]) / (LAT_TOP - LAT_BOT) * H;
    return [x, y];
  }

  fetch("https://cdn.jsdelivr.net/gh/johan/world.geo.json/countries.geo.json")
    .then(function (r) { return r.json(); })
    .then(draw)
    .catch(function () { if (wrap) wrap.style.display = "none"; });

  function drawPoly(coords) {
    coords.forEach(function (ring) {
      ctx.beginPath();
      ring.forEach(function (ll, i) {
        var p = proj(ll);
        i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]);
      });
      ctx.closePath();
      ctx.fill();
    });
  }

  function draw(geo) {
    ctx.fillStyle = "#dbe4ec";
    geo.features.forEach(function (f) {
      var g = f.geometry;
      if (!g) return;
      if (g.type === "Polygon") drawPoly(g.coordinates);
      if (g.type === "MultiPolygon") g.coordinates.forEach(drawPoly);
    });

    // route
    var pts = stops.map(function (s) { return proj(s.ll); });
    ctx.strokeStyle = "#0067b8";
    ctx.lineWidth = 2;
    ctx.setLineDash([7, 6]);
    ctx.beginPath();
    pts.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
    ctx.stroke();
    ctx.setLineDash([]);

    // stops
    var seen = {};
    stops.forEach(function (s, i) {
      var p = proj(s.ll);
      ctx.fillStyle = i === 0 ? "#f25022" : "#0067b8";
      ctx.beginPath(); ctx.arc(p[0], p[1], 6, 0, 7); ctx.fill();
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
      var label = s.e.city.split(",")[0];
      if (!seen[label]) {
        seen[label] = 1;
        ctx.fillStyle = "#171717";
        ctx.font = "600 14px 'Segoe UI', sans-serif";
        ctx.fillText(label, p[0] + 10, p[1] + 4);
      }
    });

    animatePlane(pts);
  }

  function animatePlane(pts) {
    var seg = 0, prog = 0;
    var base = canvas.toDataURL();
    var img = new Image();
    img.src = base;
    img.onload = function () { requestAnimationFrame(tick); };
    function tick() {
      prog += 0.006;
      if (prog >= 1) { prog = 0; seg = (seg + 1) % (pts.length - 1); }
      var a = pts[seg], b = pts[seg + 1];
      var x = a[0] + (b[0] - a[0]) * prog;
      var y = a[1] + (b[1] - a[1]) * prog;
      ctx.clearRect(0, 0, W, H);
      ctx.drawImage(img, 0, 0);
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(Math.atan2(b[1] - a[1], b[0] - a[0]));
      ctx.font = "22px serif";
      ctx.fillText("✈️", -11, 8);
      ctx.restore();
      requestAnimationFrame(tick);
    }
  }
})();
