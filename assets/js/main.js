/* The Urban Edit — small, dependency-free enhancements */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- "More" dropdown ---- */
  $$(".dropdown-toggle").forEach(function (btn) {
    var menu = document.getElementById(btn.getAttribute("aria-controls"));
    if (!menu) return;
    function set(open) { btn.setAttribute("aria-expanded", String(open)); menu.hidden = !open; }
    btn.addEventListener("click", function (e) { e.stopPropagation(); set(menu.hidden); });
    document.addEventListener("click", function (e) { if (!menu.contains(e.target)) set(false); });
    btn.parentElement.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { set(false); btn.focus(); }
      if (e.key === "ArrowDown" && !menu.hidden) { e.preventDefault(); var l = $$("a", menu); var i = l.indexOf(document.activeElement); (l[i + 1] || l[0]).focus(); }
      if (e.key === "ArrowUp" && !menu.hidden) { e.preventDefault(); var l2 = $$("a", menu); var j = l2.indexOf(document.activeElement); (l2[j - 1] || l2[l2.length - 1]).focus(); }
    });
    btn.parentElement.addEventListener("focusout", function (e) { if (!btn.parentElement.contains(e.relatedTarget)) set(false); });
  });

  /* ---- Search panel ---- */
  var panel = $("#search-panel");
  $$(".search-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!panel) return;
      var open = panel.hidden;
      panel.hidden = !open;
      $$(".search-toggle").forEach(function (b) { b.setAttribute("aria-expanded", String(open)); });
      if (open) { var i = $("input", panel); if (i) i.focus(); }
    });
  });

  /* ---- Mobile menu ---- */
  var mm = $("#mobile-menu"), mt = $(".menu-toggle");
  function setMenu(open) {
    if (!mm || !mt) return;
    mm.hidden = !open; mt.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("menu-open", open);
    if (open) { var f = $(".menu-close", mm); if (f) f.focus(); } else { mt.focus(); }
  }
  if (mt) mt.addEventListener("click", function () { setMenu(true); });
  if (mm) {
    $(".menu-close", mm).addEventListener("click", function () { setMenu(false); });
    mm.addEventListener("click", function (e) { if (e.target === mm) setMenu(false); });
    mm.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
      if (e.key === "Tab") { // focus trap
        var f = $$("a, button, input", mm); var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && panel && !panel.hidden) { panel.hidden = true; } });

  /* ---- Table of contents ---- */
  var body = $(".article__body"), toc = $(".toc");
  if (body && toc) {
    var heads = $$("h2[id]", body).filter(function (h) { return !h.closest(".sources"); });
    if (heads.length >= 2) {
      var list = $(".toc__list", toc);
      heads.forEach(function (h) {
        var li = document.createElement("li"), a = document.createElement("a");
        a.href = "#" + h.id; a.textContent = h.textContent; li.appendChild(a); list.appendChild(li);
      });
      toc.hidden = false;
      if ("IntersectionObserver" in window) {
        var links = $$("a", list);
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) links.forEach(function (l) { l.classList.toggle("is-active", l.getAttribute("href") === "#" + en.target.id); });
          });
        }, { rootMargin: "0px 0px -70% 0px" });
        heads.forEach(function (h) { io.observe(h); });
      }
    }
    // External links open in a new tab
    $$("a[href^='http']", body).forEach(function (a) {
      if (a.hostname !== location.hostname) { a.target = "_blank"; a.rel = "noopener"; }
    });
  }

  /* ---- Copy link ---- */
  $$(".copy-link").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = b.getAttribute("data-url");
      var done = function () { b.classList.add("is-copied"); b.setAttribute("aria-label", "Link copied"); setTimeout(function () { b.classList.remove("is-copied"); b.setAttribute("aria-label", "Copy link"); }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () {}); else { window.prompt("Copy this link:", url); }
    });
  });

  /* ---- Newsletter placeholder (no service connected yet) ---- */
  $$("form[data-newsletter-pending]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var n = $(".newsletter__note", f);
      if (n) n.textContent = "Thank you. Our newsletter launches soon — we haven’t stored your address, so please check back to subscribe.";
      f.reset();
    });
  });

  /* ---- Client-side pagination for long grids ---- */
  $$("[data-paginate]").forEach(function (grid) {
    var per = parseInt(grid.getAttribute("data-paginate"), 10) || 9;
    var items = Array.prototype.slice.call(grid.children);
    var pager = grid.nextElementSibling;
    if (items.length <= per || !pager || !pager.classList.contains("pager")) return;
    var pages = Math.ceil(items.length / per);
    var params = new URLSearchParams(location.search);
    var current = Math.min(Math.max(parseInt(params.get("page"), 10) || 1, 1), pages);
    function render(p, scroll) {
      current = p;
      items.forEach(function (it, i) { it.hidden = i < (p - 1) * per || i >= p * per; });
      pager.innerHTML = "";
      function btn(label, page, opts) {
        var b = document.createElement("button"); b.type = "button"; b.textContent = label;
        if (opts && opts.aria) b.setAttribute("aria-label", opts.aria);
        if (page === current && !(opts && opts.nav)) b.setAttribute("aria-current", "page");
        if (opts && opts.disabled) b.disabled = true;
        b.addEventListener("click", function () { render(page, true); });
        pager.appendChild(b);
      }
      btn("←", Math.max(1, p - 1), { nav: true, disabled: p === 1, aria: "Previous page" });
      for (var i = 1; i <= pages; i++) btn(String(i), i, { aria: "Page " + i });
      btn("→", Math.min(pages, p + 1), { nav: true, disabled: p === pages, aria: "Next page" });
      pager.hidden = false;
      var u = new URL(location.href);
      if (p === 1) u.searchParams.delete("page"); else u.searchParams.set("page", p);
      history.replaceState(null, "", u);
      if (scroll) grid.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    render(current, false);
  });

  /* ---- Search page ---- */
  var results = $("#search-results");
  if (results) {
    var input = $("#search-input"), status = $("#search-status");
    var q = new URLSearchParams(location.search).get("q") || "";
    input.value = q;
    var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var data = null;
    function run(term) {
      term = term.trim();
      if (!term) { results.innerHTML = ""; status.textContent = "Type a word or phrase to search every story."; return; }
      var words = term.toLowerCase().split(/\s+/).filter(Boolean);
      var hits = data.map(function (d) {
        var hay = { t: d.title.toLowerCase(), x: (d.excerpt + " " + d.tags.join(" ") + " " + d.category).toLowerCase(), b: d.body.toLowerCase() };
        var score = 0;
        for (var i = 0; i < words.length; i++) {
          var w = words[i], s = 0;
          if (hay.t.indexOf(w) > -1) s += 10;
          if (hay.x.indexOf(w) > -1) s += 4;
          if (hay.b.indexOf(w) > -1) s += 1;
          if (!s) return null;
          score += s;
        }
        return { d: d, score: score };
      }).filter(Boolean).sort(function (a, b) { return b.score - a.score; });
      var re = new RegExp("(" + words.map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|") + ")", "gi");
      var hl = function (s) { return esc(s).replace(re, "<mark>$1</mark>"); };
      status.textContent = hits.length + (hits.length === 1 ? " result" : " results") + " for “" + term + "”";
      results.innerHTML = hits.map(function (h) {
        var d = h.d;
        return '<li><p class="meta"><span>' + esc(d.category) + '</span><span aria-hidden="true">·</span><time>' + esc(d.date) + '</time></p>' +
          '<h2><a href="' + esc(d.url) + '">' + hl(d.title) + '</a></h2><p>' + hl(d.excerpt) + '</p></li>';
      }).join("");
      document.title = (term ? "Search: " + term + " | " : "") + "The Urban Edit";
    }
    status.textContent = "Loading…";
    fetch(results.getAttribute("data-index")).then(function (r) { return r.json(); }).then(function (j) {
      data = j; run(q);
      input.addEventListener("input", function () {
        run(input.value);
        var u = new URL(location.href); if (input.value) u.searchParams.set("q", input.value); else u.searchParams.delete("q"); history.replaceState(null, "", u);
      });
    }).catch(function () { status.textContent = "Search is unavailable right now. Please browse the sections instead."; });
  }
})();
