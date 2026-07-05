/* Tour globe — plots upcoming events from js/events.js on a 3D orthographic
   globe (d3-geo, countries fetched client-side from a public GeoJSON CDN).
   Auto-rotates, drag to spin, plane flies great-circle routes between stops.
   Degrades gracefully: section hides if d3 or the GeoJSON fails to load. */
(function () {
  "use strict";
  var canvas = document.getElementById("tour-map");
  if (!canvas) return;
  var wrap = document.getElementById("tour-map-section");

  function fail() { if (wrap) wrap.style.display = "none"; }
  if (typeof d3 === "undefined") { fail(); return; }

  var COORDS = {
    "london":  [-0.12, 51.51],
    "redmond": [-122.12, 47.67],
    "oslo":    [10.75, 59.91],
    "gjøvik":  [10.69, 60.79],
    "gjovik":  [10.69, 60.79],
    "orlando": [-81.38, 28.54],
    "amsterdam": [4.90, 52.37],
    "rosmalen": [5.36, 51.72],
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

  if (stops.length < 2) { fail(); return; }

  var W = 1100, H = 640, R = 290;
  canvas.width = W; canvas.height = H;
  var ctx = canvas.getContext("2d");

  var projection = d3.geoOrthographic()
    .translate([W / 2, H / 2])
    .scale(R)
    .clipAngle(90)
    .rotate([-stops[0].ll[0], -Math.max(Math.min(stops[0].ll[1], 45), -45)]);

  var path = d3.geoPath(projection, ctx);
  var graticule = d3.geoGraticule10();
  var route = { type: "LineString", coordinates: stops.map(function (s) { return s.ll; }) };
  var land = null;

  // Great-circle interpolators for the plane, one per leg
  var legs = [];
  for (var i = 0; i < stops.length - 1; i++) {
    legs.push({
      interp: d3.geoInterpolate(stops[i].ll, stops[i + 1].ll),
      dist: d3.geoDistance(stops[i].ll, stops[i + 1].ll)
    });
  }

  function visible(ll) {
    var r = projection.rotate();
    return d3.geoDistance(ll, [-r[0], -r[1]]) < Math.PI / 2 - 0.02;
  }

  var tourCountries = null; // features containing a tour stop → highlighted

  // Planar point-in-polygon (ray cast on lon/lat) — immune to ring winding order.
  function inRing(ll, ring) {
    var x = ll[0], y = ll[1], inside = false;
    for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  }
  function inPolygon(ll, rings) {
    if (!inRing(ll, rings[0])) return false;           // outside exterior
    for (var i = 1; i < rings.length; i++) if (inRing(ll, rings[i])) return false; // in a hole
    return true;
  }
  function featureContains(f, ll) {
    var g = f.geometry;
    if (!g) return false;
    if (g.type === "Polygon") return inPolygon(ll, g.coordinates);
    if (g.type === "MultiPolygon") return g.coordinates.some(function (p) { return inPolygon(ll, p); });
    return false;
  }

  fetch("https://cdn.jsdelivr.net/gh/johan/world.geo.json/countries.geo.json")
    .then(function (r) { return r.json(); })
    .then(function (geo) {
      land = geo;
      tourCountries = {
        type: "FeatureCollection",
        features: geo.features.filter(function (f) {
          return stops.some(function (s) { return featureContains(f, s.ll); });
        })
      };
      requestAnimationFrame(tick);
    })
    .catch(fail);

  /* ---- interaction: drag to spin ---- */
  var dragging = false, lastX = 0, lastY = 0, lastInteraction = 0;
  canvas.style.cursor = "grab";
  canvas.style.touchAction = "none";

  canvas.addEventListener("pointerdown", function (e) {
    dragging = true; lastX = e.clientX; lastY = e.clientY;
    canvas.setPointerCapture(e.pointerId);
    canvas.style.cursor = "grabbing";
  });
  canvas.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    var r = projection.rotate();
    var k = 0.35 * (W / canvas.getBoundingClientRect().width);
    projection.rotate([
      r[0] + (e.clientX - lastX) * k,
      Math.max(-80, Math.min(80, r[1] - (e.clientY - lastY) * k))
    ]);
    lastX = e.clientX; lastY = e.clientY;
    lastInteraction = performance.now();
  });
  function endDrag() { dragging = false; canvas.style.cursor = "grab"; lastInteraction = performance.now(); }
  canvas.addEventListener("pointerup", endDrag);
  canvas.addEventListener("pointercancel", endDrag);

  /* ---- render loop ---- */
  var seg = 0, prog = 0;

  function tick(now) {
    // auto-rotate, paused while dragging and for 3s after
    if (!dragging && now - lastInteraction > 3000) {
      var r = projection.rotate();
      projection.rotate([r[0] + 0.06, r[1]]);
    }

    // plane progress (slower over longer legs looks natural: constant angular speed)
    prog += 0.0045 / Math.max(legs[seg].dist, 0.15) * 0.9;
    if (prog >= 1) { prog = 0; seg = (seg + 1) % legs.length; }

    render();
    requestAnimationFrame(tick);
  }

  var CX = W / 2, CY = H / 2;

  function render() {
    ctx.clearRect(0, 0, W, H);

    // atmosphere glow behind the globe
    var glow = ctx.createRadialGradient(CX, CY, R * 0.95, CX, CY, R + 26);
    glow.addColorStop(0, "rgba(0,120,215,.35)");
    glow.addColorStop(1, "rgba(0,120,215,0)");
    ctx.fillStyle = glow;
    ctx.beginPath(); ctx.arc(CX, CY, R + 26, 0, 7); ctx.fill();

    // ocean — lit from the upper left for a 3D feel
    var ocean = ctx.createRadialGradient(CX - R * 0.4, CY - R * 0.4, R * 0.1, CX, CY, R);
    ocean.addColorStop(0, "#8ec9f0");
    ocean.addColorStop(0.6, "#4a9fd8");
    ocean.addColorStop(1, "#1e5e94");
    ctx.beginPath(); path({ type: "Sphere" });
    ctx.fillStyle = ocean; ctx.fill();

    // graticule
    ctx.beginPath(); path(graticule);
    ctx.strokeStyle = "rgba(255,255,255,.14)"; ctx.lineWidth = 1; ctx.stroke();

    // land
    ctx.beginPath(); path(land);
    ctx.fillStyle = "#9fce8b"; ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,.55)"; ctx.lineWidth = .6; ctx.stroke();

    // countries on the tour — highlighted
    if (tourCountries) {
      ctx.beginPath(); path(tourCountries);
      ctx.fillStyle = "#ffd166"; ctx.fill();
      ctx.strokeStyle = "rgba(255,255,255,.8)"; ctx.lineWidth = .8; ctx.stroke();
    }

    // day/night-style edge shading to round the sphere
    var shade = ctx.createRadialGradient(CX - R * 0.4, CY - R * 0.4, R * 0.2, CX, CY, R * 1.05);
    shade.addColorStop(0, "rgba(255,255,255,.10)");
    shade.addColorStop(0.55, "rgba(0,0,0,0)");
    shade.addColorStop(1, "rgba(4,28,52,.38)");
    ctx.beginPath(); path({ type: "Sphere" });
    ctx.fillStyle = shade; ctx.fill();
    ctx.strokeStyle = "rgba(20,60,100,.5)"; ctx.lineWidth = 1.5; ctx.stroke();

    // route (geoPath draws LineStrings as great circles, clipped to the front)
    ctx.beginPath(); path(route);
    ctx.strokeStyle = "rgba(255,255,255,.95)"; ctx.lineWidth = 2.2;
    ctx.setLineDash([7, 6]); ctx.stroke(); ctx.setLineDash([]);

    // stops + labels
    var seen = {};
    stops.forEach(function (s, i) {
      if (!visible(s.ll)) return;
      var p = projection(s.ll);
      ctx.fillStyle = i === 0 ? "#f25022" : "#0067b8";
      ctx.beginPath(); ctx.arc(p[0], p[1], 6, 0, 7); ctx.fill();
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
      var label = s.e.city.split(",")[0];
      if (!seen[label]) {
        seen[label] = 1;
        ctx.font = "600 14px 'Segoe UI', sans-serif";
        ctx.strokeStyle = "rgba(255,255,255,.85)"; ctx.lineWidth = 3;
        ctx.strokeText(label, p[0] + 10, p[1] + 4);
        ctx.fillStyle = "#12293f";
        ctx.fillText(label, p[0] + 10, p[1] + 4);
      }
    });

    // plane on the current leg
    var ll = legs[seg].interp(prog);
    if (visible(ll)) {
      var p = projection(ll);
      var ahead = projection(legs[seg].interp(Math.min(prog + 0.02, 1)));
      ctx.save();
      ctx.translate(p[0], p[1]);
      ctx.rotate(Math.atan2(ahead[1] - p[1], ahead[0] - p[0]));
      ctx.font = "22px serif";
      ctx.fillText("✈️", -11, 8);
      ctx.restore();
    }
  }
})();
