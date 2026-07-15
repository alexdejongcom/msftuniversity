/* Course evaluation — shown for the course that is currently running
 * (grace period: up to 3 days after it ends), same gating as the
 * certificate. Data comes from js/events.js; submissions go to
 * /api/evaluation. One submission per course per browser. */
(function () {
  "use strict";
  var form = document.getElementById("eval-form");
  if (!form) return;
  var section = document.getElementById("eval-section");
  var notice = document.getElementById("eval-notice");
  var result = document.getElementById("eval-result");
  var submitBtn = document.getElementById("eval-submit");

  var GRACE_DAYS = 3;

  function runningEvent() {
    var t = new Date(); t.setHours(0, 0, 0, 0);
    var evs = (typeof EVENTS !== "undefined" ? EVENTS : []);
    var graceMatch = null;
    for (var i = 0; i < evs.length; i++) {
      var e = evs[i];
      var start = new Date(e.date + "T00:00:00");
      var end = new Date((e.end || e.date) + "T00:00:00");
      if (start <= t && t <= end) return e; // actually running today wins
      var graceEnd = new Date(end); graceEnd.setDate(graceEnd.getDate() + GRACE_DAYS);
      if (start <= t && t <= graceEnd && (!graceMatch || end > graceMatch._end)) {
        graceMatch = e; graceMatch._end = end;
      }
    }
    return graceMatch; // most recently ended course, if nothing runs today
  }

  var ev = runningEvent();
  if (!ev) {
    if (form) form.style.display = "none";
    if (notice) notice.style.display = "block";
    return;
  }

  var doneKey = "mu-eval-" + ev.date;
  function thanks(already) {
    form.style.display = "none";
    result.innerHTML =
      '<p style="font-size:17px">✅ ' +
      (already ? "You already evaluated this course — thank you!"
               : "Thank you! Your evaluation helps make the next course even better.") +
      "</p>";
  }
  try { if (localStorage.getItem(doneKey)) { thanks(true); return; } } catch (e) {}

  // ---- star rating widgets ----
  var ratings = {};
  Array.prototype.forEach.call(form.querySelectorAll(".eval-stars"), function (row) {
    var field = row.getAttribute("data-field");
    for (var i = 1; i <= 5; i++) {
      (function (v) {
        var b = document.createElement("button");
        b.type = "button";
        b.textContent = "★";
        b.setAttribute("aria-label", v + " of 5");
        b.style.cssText = "font-size:28px;background:none;border:none;cursor:pointer;padding:2px 4px;color:var(--border)";
        b.addEventListener("click", function () {
          ratings[field] = v;
          Array.prototype.forEach.call(row.children, function (s, idx) {
            s.style.color = idx < v ? "#ffb900" : "var(--border)";
          });
          row.removeAttribute("data-missing");
        });
        row.appendChild(b);
      })(i);
    }
  });

  submitBtn.addEventListener("click", function () {
    var pace = (form.querySelector('input[name="eval-pace"]:checked') || {}).value;
    var missing = [];
    ["content", "instructor", "overall"].forEach(function (f) {
      if (!ratings[f]) missing.push(f);
    });
    if (missing.length || !pace) {
      result.innerHTML = '<p style="color:#d13438">Please rate all three categories and pick a pace before submitting.</p>';
      return;
    }
    result.innerHTML = "";
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    var payload = {
      course: ev.title || "",
      date: ev.date,
      content: ratings.content,
      instructor: ratings.instructor,
      overall: ratings.overall,
      pace: pace,
      comment: (document.getElementById("eval-comment").value || "").trim(),
    };

    fetch("/api/evaluation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); })
      .then(function () {
        try { localStorage.setItem(doneKey, "1"); } catch (e) {}
        window.__achieve && window.__achieve("eval");
        thanks(false);
      })
      .catch(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = "Submit evaluation";
        result.innerHTML = '<p style="color:#d13438">Could not send your evaluation right now — please try again in a minute.</p>';
      });
  });
})();
