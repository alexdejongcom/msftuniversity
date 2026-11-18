/* The Briefing — sign-up forms. Enhances every <form class="nl-form">:
 * posts to /api/newsletter/subscribe and shows the answer inline.
 * The hidden "website" field is a honeypot for bots. */
(function () {
  "use strict";
  var forms = document.querySelectorAll("form.nl-form");
  Array.prototype.forEach.call(forms, function (form) {
    var input = form.querySelector("input[type=email]");
    var btn = form.querySelector("button");
    var msg = form.querySelector(".nl-msg");
    if (!msg) { msg = document.createElement("div"); msg.className = "nl-msg"; msg.setAttribute("role", "status"); form.appendChild(msg); }
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var hp = form.querySelector("input[name=website]");
      msg.className = "nl-msg"; msg.textContent = "";
      btn.disabled = true;
      fetch("/api/newsletter/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: input.value, website: hp ? hp.value : "" }),
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (b) { return { ok: r.ok, b: b }; }); })
        .then(function (res) {
          if (res.ok) {
            msg.className = "nl-msg ok";
            msg.textContent = "Almost there — check your inbox and click the confirmation link.";
            input.value = "";
            if (window.__achieve) window.__achieve("newsletter");
          } else {
            msg.className = "nl-msg err";
            msg.textContent = (res.b && res.b.message) || "Something went wrong. Please try again.";
          }
        })
        .catch(function () { msg.className = "nl-msg err"; msg.textContent = "You seem to be offline. Please try again."; })
        .then(function () { btn.disabled = false; });
    });
  });
})();
