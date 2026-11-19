/* The Redmond Report — editor (newsletter-admin.html).
 * Requires the SWA role "newsletter-admin"; the API enforces it too.
 * All feed text goes through textContent / value — never innerHTML. */
(function () {
  "use strict";
  var API = "/api/newsletter/admin/";
  var app = document.getElementById("nla-app");
  var who = document.getElementById("nla-who");
  var state = null, issue = null, dirty = false, pollTimer = null;

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") n.textContent = attrs[k];
      else if (k === "style") n.style.cssText = attrs[k];
      else if (k === "value") n.value = attrs[k];
      else if (k.slice(0, 2) === "on") n.addEventListener(k.slice(2), attrs[k]);
      else if (k in n && typeof attrs[k] !== "string") n[k] = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return n;
  }
  function api(method, action, body) {
    return fetch(API + action, {
      method: method, headers: body ? { "Content-Type": "application/json" } : {},
      body: body ? JSON.stringify(body) : undefined, credentials: "same-origin",
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (b) {
        if (!r.ok) throw new Error(b.error || ("HTTP " + r.status));
        return b;
      });
    });
  }
  function toast(text, bad) {
    var t = el("div", { text: text, style: "position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:9999;padding:12px 20px;border-radius:8px;color:#fff;font-weight:600;box-shadow:0 8px 24px rgba(0,0,0,.2);background:" + (bad ? "#a4262c" : "#0e700e") });
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 3500);
  }
  function fmt(iso) { return iso ? new Date(iso).toLocaleString("en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }) : ""; }

  /* ---------- sign-in ---------- */
  fetch("/.auth/me").then(function (r) { return r.json(); }).then(function (me) {
    var p = me && me.clientPrincipal;
    if (!p || (p.userRoles || []).indexOf("newsletter-admin") < 0) {
      who.textContent = p ? "Signed in as " + p.userDetails + " — but without the newsletter-admin role." : "You're not signed in.";
      document.getElementById("nla-signin").hidden = false;
      return;
    }
    who.textContent = "Signed in as " + p.userDetails + ". ";
    who.appendChild(el("a", { href: "/.auth/logout?post_logout_redirect_uri=/", text: "Sign out", style: "color:#fff;text-decoration:underline" }));
    app.hidden = false;
    loadState();
  }).catch(function () {
    who.textContent = "Couldn't check your sign-in (this page only works on the live site).";
    document.getElementById("nla-signin").hidden = false;
  });

  window.addEventListener("beforeunload", function (e) { if (dirty) { e.preventDefault(); e.returnValue = ""; } });

  /* ---------- overview ---------- */
  function loadState(openId) {
    return api("GET", "state").then(function (s) {
      state = s;
      var target = openId || (s.issues.find(function (i) { return i.status !== "sent"; }) || {}).id;
      renderOverview();
      if (target) openIssue(target); else renderEditor();
    }).catch(function (e) { app.textContent = "Could not load: " + e.message; });
  }

  function stat(n, label) {
    return el("div", { class: "card", style: "padding:16px 18px;flex:1;min-width:140px" }, [
      el("div", { text: String(n), style: "font-size:28px;font-weight:700;color:var(--blue-darker)" }),
      el("div", { text: label, style: "font-size:13px;color:var(--ink-faint)" }),
    ]);
  }

  function renderOverview() {
    app.innerHTML = "";
    var c = state.configured, missing = [];
    if (!c.acs) missing.push("ACS_CONNECTION_STRING");
    if (!c.from) missing.push("NL_FROM");
    if (!c.admin) missing.push("NL_ADMIN_EMAIL");
    if (!c.cron) missing.push("NL_CRON_KEY");
    if (missing.length) app.appendChild(el("div", { class: "card", style: "border-left:4px solid #c19c00;background:#fff8e1;margin-bottom:20px" }, [
      el("b", { text: "Setup incomplete. " }), "Missing app settings: " + missing.join(", ") + ". See DEPLOY.md → Newsletter.",
    ]));
    app.appendChild(el("div", { style: "display:flex;gap:14px;flex-wrap:wrap;margin-bottom:24px" }, [
      stat(state.subscribers.active, "confirmed subscribers"),
      stat(state.subscribers.pending, "awaiting confirmation"),
      stat(state.issues.filter(function (i) { return i.status === "sent"; }).length, "issues sent"),
      el("div", { class: "card", style: "padding:16px 18px;flex:2;min-width:220px;display:flex;flex-direction:column;gap:8px;justify-content:center" }, [
        el("button", { class: "btn btn-blue", text: "Build a new draft from the latest news", style: "cursor:pointer;border:0", onclick: newDraft }),
        el("a", { href: API + "subscribers.csv", text: "Export subscribers (CSV)", style: "font-size:13.5px" }),
      ]),
    ]));
    var list = el("ul", { class: "resource-list" });
    state.issues.forEach(function (i) {
      var badge = i.status === "sent" ? "Sent " + fmt(i.sentAt) + " · " + i.sent + "/" + i.total : i.status === "sending" ? "Sending · " + i.sent + "/" + i.total : "Draft · " + fmt(i.updatedAt || i.createdAt);
      list.appendChild(el("li", {}, [el("a", { href: "#", onclick: function (e) { e.preventDefault(); openIssue(i.id); } }, [
        el("span", { text: i.subject || "(no subject)" }), el("span", { class: "desc", text: badge }),
      ])]));
    });
    app.appendChild(el("details", { class: "card resource-group", style: "margin-bottom:24px", open: !state.issues.length }, [
      el("summary", { text: "All issues (" + state.issues.length + ")", style: "cursor:pointer;font-weight:600" }), list,
    ]));
    app.appendChild(el("div", { id: "nla-editor" }));
  }

  function newDraft() {
    if (dirty && !confirm("Discard unsaved changes?")) return;
    toast("Collecting the latest news…");
    api("POST", "draft", {}).then(function (d) { dirty = false; loadState(d.id); toast("Draft ready"); })
      .catch(function (e) { toast(e.message, true); });
  }

  function openIssue(id) {
    if (dirty && issue && issue.id !== id && !confirm("Discard unsaved changes?")) return;
    api("GET", "issue?id=" + encodeURIComponent(id)).then(function (it) { issue = it; dirty = false; renderEditor(); })
      .catch(function (e) { toast(e.message, true); });
  }

  /* ---------- editor ---------- */
  function field(label, input, help) {
    return el("label", { style: "display:block;margin-bottom:18px" }, [
      el("div", { text: label, style: "font-weight:600;margin-bottom:6px" }), input,
      help ? el("div", { text: help, style: "font-size:12.5px;color:var(--ink-faint);margin-top:4px" }) : null,
    ]);
  }
  var INPUT = "width:100%;padding:10px 12px;font:inherit;font-size:15px;border:1px solid var(--border);border-radius:6px;";
  function mark() { dirty = true; var s = document.getElementById("nla-save"); if (s) s.textContent = "Save draft •"; }

  function renderEditor() {
    var host = document.getElementById("nla-editor");
    if (!host) return;
    host.innerHTML = "";
    clearTimeout(pollTimer);
    if (!issue) { host.appendChild(el("p", { text: "No draft yet — build one from the latest news above.", style: "color:var(--ink-faint)" })); return; }
    var ro = issue.status !== "draft";

    if (issue.status === "sending") {
      var pct = issue.total ? Math.round((issue.sent + issue.failed) / issue.total * 100) : 0;
      host.appendChild(el("div", { class: "card", style: "margin-bottom:20px" }, [
        el("b", { text: "Sending: " + issue.sent + " of " + issue.total + " delivered to the mail service" + (issue.failed ? " · " + issue.failed + " failed" : "") }),
        el("div", { style: "height:8px;background:var(--bg-alt);border-radius:4px;margin:10px 0" }, [el("div", { style: "height:8px;border-radius:4px;background:var(--blue);width:" + pct + "%" })]),
        el("div", { text: "Azure's send limits spread large lists over time. Keep this page open to speed things up — the hourly scheduler finishes it otherwise.", style: "font-size:13px;color:var(--ink-faint)" }),
      ]));
      pumpSending();
    }

    var subject = el("input", { value: issue.subject, style: INPUT + "font-size:18px;font-weight:600", disabled: ro, oninput: mark });
    var intro = el("textarea", { value: issue.intro, rows: 6, style: INPUT, disabled: ro, oninput: mark, placeholder: "Your take on this fortnight — what stood out, what people should act on. Blank line = new paragraph." });
    var outro = el("textarea", { value: issue.outro, rows: 3, style: INPUT, disabled: ro, oninput: mark, placeholder: "Optional closing note — a tip, a question, a plug for a course." });
    host.appendChild(field("Subject", subject));
    host.appendChild(field("Your introduction", intro));

    var groups = [["release", "Release notes"], ["roadmap", "On the roadmap"], ["blog", "From the Microsoft blogs"]];
    var counter = el("span", { style: "font-weight:400;color:var(--ink-faint)" });
    function count() { counter.textContent = " · " + issue.items.filter(function (i) { return i.include; }).length + " selected"; }
    count();
    host.appendChild(el("h3", { style: "margin:8px 0 4px" }, ["News items", counter]));
    host.appendChild(el("p", { text: "Tick what goes in. Add a line on why it matters — that's what makes people open the next one.", style: "font-size:13.5px;color:var(--ink-faint);margin-bottom:12px" }));
    groups.forEach(function (g) {
      var rows = issue.items.filter(function (i) { return i.kind === g[0]; });
      if (!rows.length) return;
      var box = el("div", { class: "card", style: "margin-bottom:16px;padding:18px 20px" }, [el("div", { text: g[1], style: "font-weight:700;margin-bottom:8px" })]);
      rows.forEach(function (it) {
        var note = el("textarea", { value: it.note || "", rows: 2, style: INPUT + "font-size:14px;margin-top:6px", disabled: ro, placeholder: "Why it matters (optional)", oninput: function () { it.note = note.value; mark(); } });
        note.hidden = !it.include;
        var cb = el("input", { type: "checkbox", checked: !!it.include, disabled: ro, style: "margin-top:4px;transform:scale(1.2)", onchange: function () { it.include = cb.checked; note.hidden = !cb.checked; count(); mark(); } });
        box.appendChild(el("div", { style: "display:flex;gap:12px;padding:10px 0;border-top:1px solid var(--border)" }, [
          cb,
          el("div", { style: "flex:1;min-width:0" }, [
            el("div", { style: "font-size:12px;font-weight:700;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.4px" }, [it.source + (it.meta ? " · " + it.meta : "")]),
            el("a", { href: it.link, target: "_blank", rel: "noopener", text: it.title, style: "font-weight:600" }),
            note,
          ]),
        ]));
      });
      host.appendChild(box);
    });
    if (!issue.items.length) host.appendChild(el("p", { text: "No new items since the last issue.", style: "color:var(--ink-faint)" }));

    if (issue.events.length) {
      var evBox = el("div", { class: "card", style: "margin-bottom:16px;padding:18px 20px" }, [el("div", { text: "Upcoming courses & events", style: "font-weight:700;margin-bottom:8px" })]);
      issue.events.forEach(function (ev) {
        var cb = el("input", { type: "checkbox", checked: ev.include !== false, disabled: ro, onchange: function () { ev.include = cb.checked; mark(); } });
        evBox.appendChild(el("label", { style: "display:flex;gap:10px;padding:6px 0;align-items:center" }, [cb, ev.date + (ev.end ? " → " + ev.end : "") + "  " + ev.title + (ev.city ? " (" + ev.city + ")" : "")]));
      });
      host.appendChild(evBox);
    }
    host.appendChild(field("Closing note", outro));

    var bar = el("div", { style: "position:sticky;bottom:0;background:#fff;border-top:1px solid var(--border);padding:14px 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center;z-index:5" });
    function collect() { issue.subject = subject.value; issue.intro = intro.value; issue.outro = outro.value; return issue; }
    function save() {
      return api("POST", "save", collect()).then(function (it) { issue = it; dirty = false; var s = document.getElementById("nla-save"); if (s) s.textContent = "Save draft"; toast("Saved"); return it; });
    }
    if (!ro) {
      bar.appendChild(el("button", { id: "nla-save", class: "btn btn-outline", text: "Save draft", style: "cursor:pointer", onclick: function () { save().catch(function (e) { toast(e.message, true); }); } }));
      bar.appendChild(el("button", { class: "btn btn-outline", text: "Preview", style: "cursor:pointer", onclick: function () { save().then(preview).catch(function (e) { toast(e.message, true); }); } }));
      bar.appendChild(el("button", { class: "btn btn-outline", text: "Send me a test", style: "cursor:pointer", onclick: function () {
        save().then(function () { return api("POST", "test", { id: issue.id }); }).then(function (r) { toast("Test sent to " + r.to); }).catch(function (e) { toast(e.message, true); });
      } }));
      bar.appendChild(el("button", { class: "btn btn-blue", text: "Send to " + state.subscribers.active + " subscribers…", style: "cursor:pointer;border:0;margin-left:auto", onclick: function () {
        var n = state.subscribers.active;
        if (!confirm("Send “" + subject.value + "” to " + n + " confirmed subscriber" + (n === 1 ? "" : "s") + "? This can't be undone.")) return;
        save().then(function () { return api("POST", "send", { id: issue.id }); })
          .then(function (r) { toast("Sending started — " + r.sentNow + " of " + r.total + " out"); loadState(issue.id); })
          .catch(function (e) { toast(e.message, true); });
      } }));
      bar.appendChild(el("button", { class: "btn", text: "Delete draft", style: "cursor:pointer;color:#a4262c;background:none", onclick: function () {
        if (!confirm("Delete this draft?")) return;
        api("POST", "delete", { id: issue.id }).then(function () { issue = null; dirty = false; loadState(); }).catch(function (e) { toast(e.message, true); });
      } }));
    } else {
      bar.appendChild(el("button", { class: "btn btn-outline", text: "Preview", style: "cursor:pointer", onclick: preview }));
      if (issue.status === "sent") bar.appendChild(el("a", { class: "btn btn-outline", href: "/api/newsletter/issue?id=" + issue.id, target: "_blank", text: "Public web version" }));
    }
    host.appendChild(bar);
  }

  function preview() {
    fetch(API + "preview?id=" + encodeURIComponent(issue.id), { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (html) {
      var shade = el("div", { style: "position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9998;display:flex;align-items:center;justify-content:center;padding:20px", onclick: function (e) { if (e.target === shade) shade.remove(); } });
      var frame = el("iframe", { title: "Preview", style: "width:min(720px,100%);height:min(90vh,1000px);border:0;border-radius:10px;background:#f2f4f7" });
      frame.setAttribute("sandbox", "");
      frame.srcdoc = html;
      shade.appendChild(frame);
      document.body.appendChild(shade);
    });
  }

  function pumpSending() {
    pollTimer = setTimeout(function () {
      fetch("/api/newsletter/tick", { method: "POST", credentials: "same-origin" }).then(function (r) { return r.json(); })
        .then(function (t) { return api("GET", "issue?id=" + encodeURIComponent(issue.id)).then(function (it) { issue = it; if (it.status === "sent") { toast("All sent!"); loadState(it.id); } else renderEditor(); }); })
        .catch(function () { pumpSending(); });
    }, 65000);
  }
})();
