/* Installable web app — service worker registration and the install prompt.

   Registration is deferred to the load event so it never competes with the
   page's own resources. On Chrome and Edge we capture beforeinstallprompt and
   show our own button; iOS gives no such event, so Safari users are told to
   use Share ▸ Add to Home Screen instead. Either way the banner shows once
   and is dismissible for good. */
(function () {
  "use strict";
  if (location.protocol !== "https:" && location.hostname !== "localhost") return;

  /* ---------- service worker ---------- */
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").then(function (reg) {
        /* A new version is waiting: activate it so the next load is current. */
        reg.addEventListener("updatefound", function () {
          var sw = reg.installing;
          if (!sw) return;
          sw.addEventListener("statechange", function () {
            if (sw.state === "installed" && navigator.serviceWorker.controller) {
              sw.postMessage("SKIP_WAITING");
            }
          });
        });
      }).catch(function () { /* nothing to do — the site works without it */ });

      var reloading = false;
      navigator.serviceWorker.addEventListener("controllerchange", function () {
        if (reloading) return;
        reloading = true;
        location.reload();
      });
    });
  }

  /* ---------- install prompt ---------- */
  var DISMISSED = "msftu-install-dismissed";
  var standalone = window.matchMedia("(display-mode: standalone)").matches ||
                   window.navigator.standalone === true;
  if (standalone) return;                       // already installed
  try { if (localStorage.getItem(DISMISSED)) return; } catch (e) {}

  var deferred = null;

  function banner(actionLabel, onAction, hint) {
    var bar = document.createElement("div");
    bar.id = "msftu-install";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Install this app");
    bar.style.cssText =
      "position:fixed;left:16px;right:16px;bottom:16px;z-index:99990;max-width:520px;" +
      "margin:0 auto;background:#fff;border:1px solid #e0e0e0;border-radius:8px;" +
      "box-shadow:0 6.4px 14.4px rgba(0,0,0,.12),0 1.2px 3.6px rgba(0,0,0,.09);" +
      "padding:14px 16px;display:flex;gap:13px;align-items:center;" +
      "font-family:'Segoe UI Variable Text','Segoe UI',-apple-system,sans-serif";

    var icon = document.createElement("img");
    icon.src = "/assets/app/icon-192.png";
    icon.alt = "";
    icon.width = 40; icon.height = 40;
    icon.style.cssText = "border-radius:9px;flex:none";
    bar.appendChild(icon);

    var text = document.createElement("div");
    text.style.cssText = "flex:1;min-width:0;line-height:1.35";
    var t1 = document.createElement("strong");
    t1.textContent = "Install Microsoft University";
    t1.style.cssText = "display:block;font-size:14.5px;color:#171717";
    var t2 = document.createElement("span");
    t2.textContent = hint;
    t2.style.cssText = "font-size:12.5px;color:#616161";
    text.appendChild(t1); text.appendChild(t2);
    bar.appendChild(text);

    if (onAction) {
      var go = document.createElement("button");
      go.type = "button";
      go.textContent = actionLabel;
      go.style.cssText =
        "flex:none;background:#0067b8;color:#fff;border:0;border-radius:6px;" +
        "padding:9px 15px;font:inherit;font-size:14px;font-weight:600;cursor:pointer";
      go.addEventListener("click", onAction);
      bar.appendChild(go);
    }

    var close = document.createElement("button");
    close.type = "button";
    close.setAttribute("aria-label", "Dismiss");
    close.textContent = "×";
    close.style.cssText =
      "flex:none;background:none;border:0;color:#616161;font-size:22px;line-height:1;" +
      "cursor:pointer;padding:2px 4px";
    close.addEventListener("click", function () {
      try { localStorage.setItem(DISMISSED, "1"); } catch (e) {}
      bar.remove();
    });
    bar.appendChild(close);

    document.body.appendChild(bar);
    return bar;
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferred = e;
    var bar = banner("Install", function () {
      bar.remove();
      deferred.prompt();
      deferred.userChoice.then(function () {
        try { localStorage.setItem(DISMISSED, "1"); } catch (err) {}
        deferred = null;
      });
    }, "Works offline — the whole exam prep hub comes with it.");
  });

  /* iOS has no install event; Safari needs the Share sheet. */
  var iOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  var safari = /^((?!chrome|android|crios|fxios|edgios).)*safari/i.test(navigator.userAgent);
  if (iOS && safari) {
    window.addEventListener("load", function () {
      setTimeout(function () {
        banner(null, null, "Tap Share, then Add to Home Screen. Works offline after that.");
      }, 2500);
    });
  }
})();
