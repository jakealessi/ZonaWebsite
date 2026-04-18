(function () {
  "use strict";

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function closeNav() {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
  }

  function openNav() {
    if (!nav || !toggle) return;
    nav.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Close menu");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) closeNav();
      else openNav();
    });

    nav.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function () {
        closeNav();
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeNav();
    });
  }

  function renderItemList(items) {
    var ul = document.createElement("ul");
    ul.className = "menu-items";
    items.forEach(function (it) {
      var li = document.createElement("li");
      var strong = document.createElement("strong");
      strong.textContent = it.name;
      li.appendChild(strong);
      if (it.desc) {
        var span = document.createElement("span");
        span.className = "menu-desc";
        span.textContent = it.desc;
        li.appendChild(span);
      }
      ul.appendChild(li);
    });
    return ul;
  }

  function renderSection(sec, index) {
    var details = document.createElement("details");
    details.className = "menu-details";
    if (index === 0) details.open = true;

    var summary = document.createElement("summary");
    summary.textContent = sec.title;
    details.appendChild(summary);

    var inner = document.createElement("div");
    inner.className = "menu-inner";

    if (sec.intro) {
      var intro = document.createElement("p");
      intro.className = "menu-intro";
      intro.textContent = sec.intro;
      inner.appendChild(intro);
    }

    if (sec.items && sec.items.length) {
      inner.appendChild(renderItemList(sec.items));
    }

    if (sec.groups) {
      sec.groups.forEach(function (g) {
        var h = document.createElement("h4");
        h.className = "menu-subhead";
        h.textContent = g.groupTitle;
        inner.appendChild(h);
        if (g.note) {
          var np = document.createElement("p");
          np.className = "menu-intro";
          np.textContent = g.note;
          inner.appendChild(np);
        }
        inner.appendChild(renderItemList(g.items));
      });
    }

    details.appendChild(inner);
    return details;
  }

  function mountMenu(sections, rootId) {
    var root = document.getElementById(rootId);
    if (!root || !sections) return;
    root.innerHTML = "";
    sections.forEach(function (sec, i) {
      root.appendChild(renderSection(sec, i));
    });
  }

  mountMenu(window.ZONA_DINING, "dining-menu-root");
  mountMenu(window.ZONA_CATERING, "catering-menu-root");

  var tabs = document.querySelectorAll(".menu-tab");
  var panelDining = document.getElementById("menu-panel-dining");
  var panelCatering = document.getElementById("menu-panel-catering");

  function openMenuPanel(panelName) {
    if (!tabs.length || !panelDining || !panelCatering) return;
    tabs.forEach(function (t) {
      var active = t.getAttribute("data-panel") === panelName;
      t.classList.toggle("is-active", active);
      t.setAttribute("aria-selected", active ? "true" : "false");
    });
    if (panelName === "dining") {
      panelDining.hidden = false;
      panelCatering.hidden = true;
    } else {
      panelDining.hidden = true;
      panelCatering.hidden = false;
    }
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      openMenuPanel(tab.getAttribute("data-panel") || "dining");
    });
  });

  function pad2(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function toISODateLocal(d) {
    return d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate());
  }

  function parseISODateLocal(iso) {
    var p = iso.split("-");
    return new Date(parseInt(p[0], 10), parseInt(p[1], 10) - 1, parseInt(p[2], 10));
  }

  function openingMinutes(day) {
    return day === 0 ? 11 * 60 : 10 * 60;
  }

  function closingMinutes(day) {
    if (day === 0) return 22 * 60;
    if (day >= 1 && day <= 4) return 21 * 60;
    if (day === 5) return 22 * 60;
    return 23 * 60;
  }

  function nextSlotFloorFromNowMinutes() {
    var d = new Date();
    var c = d.getHours() * 60 + d.getMinutes();
    var floor = Math.floor(c / 30) * 30;
    return c > floor ? floor + 30 : floor;
  }

  function isSameLocalDay(iso, ref) {
    return (
      iso ===
      ref.getFullYear() + "-" + pad2(ref.getMonth() + 1) + "-" + pad2(ref.getDate())
    );
  }

  function formatMinutes12h(totalMinutes) {
    var h = Math.floor(totalMinutes / 60);
    var m = totalMinutes % 60;
    var period = h >= 12 ? "PM" : "AM";
    var hr = h % 12;
    if (hr === 0) hr = 12;
    return hr + ":" + pad2(m) + " " + period;
  }

  function minutesToValue(totalMinutes) {
    return pad2(Math.floor(totalMinutes / 60)) + ":" + pad2(totalMinutes % 60);
  }

  function formatDateLong(iso) {
    var d = parseISODateLocal(iso);
    return d.toLocaleDateString(undefined, {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  var dateInput = document.getElementById("res-date");
  var partySelect = document.getElementById("res-party");
  var timeSelect = document.getElementById("res-time");
  var timeHint = document.getElementById("res-time-hint");

  function refillTimeOptions() {
    if (!dateInput || !timeSelect) return;

    var iso = dateInput.value;
    timeSelect.innerHTML = "";
    timeSelect.disabled = true;
    timeSelect.required = false;

    if (!iso) {
      var o0 = document.createElement("option");
      o0.value = "";
      o0.textContent = "Select a date first…";
      timeSelect.appendChild(o0);
      if (timeHint) {
        timeHint.textContent =
          "Times shown match our opening hours for the day you pick (30-minute slots).";
      }
      return;
    }

    var d = parseISODateLocal(iso);
    var day = d.getDay();
    var openM = openingMinutes(day);
    var closeM = closingMinutes(day);
    var now = new Date();
    var minBook = isSameLocalDay(iso, now) ? nextSlotFloorFromNowMinutes() : null;

    var slots = [];
    var t;
    for (t = openM; t <= closeM; t += 30) {
      if (minBook !== null && t < minBook) continue;
      slots.push(t);
    }

    if (!slots.length) {
      var ox = document.createElement("option");
      ox.value = "";
      ox.textContent = "No reservation times left for this date";
      timeSelect.appendChild(ox);
      timeSelect.disabled = true;
      timeSelect.required = false;
      if (timeHint) {
        timeHint.textContent =
          "No times available for this day (we may be closed or past today’s seating). Choose another date.";
      }
      return;
    }

    var ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "Select time…";
    timeSelect.appendChild(ph);

    slots.forEach(function (m) {
      var opt = document.createElement("option");
      opt.value = minutesToValue(m);
      opt.textContent = formatMinutes12h(m);
      timeSelect.appendChild(opt);
    });

    timeSelect.disabled = false;
    timeSelect.required = true;
    if (timeHint) {
      timeHint.textContent =
        "Showing times for " +
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][day] +
        " within " +
        formatMinutes12h(openM) +
        " – " +
        formatMinutes12h(closeM) +
        " (our hours that day).";
    }
  }

  if (partySelect) {
    var i;
    for (i = 1; i <= 30; i += 1) {
      var po = document.createElement("option");
      po.value = String(i);
      po.textContent = String(i);
      partySelect.appendChild(po);
    }
  }

  function setReservationDateBounds() {
    if (!dateInput) return;
    var today = new Date();
    dateInput.min = toISODateLocal(today);
    var maxD = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 120);
    dateInput.max = toISODateLocal(maxD);
  }

  if (dateInput) {
    setReservationDateBounds();
    dateInput.value = dateInput.min;

    dateInput.addEventListener("change", function () {
      refillTimeOptions();
      var fs = document.getElementById("form-status");
      if (fs) fs.textContent = "";
    });
  }

  refillTimeOptions();

  var form = document.getElementById("reservation-form");
  var statusEl = document.getElementById("form-status");

  if (form && statusEl) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var fd = new FormData(form);
      var dateIso = fd.get("date");
      var timeLabel =
        timeSelect && timeSelect.selectedIndex > 0
          ? timeSelect.options[timeSelect.selectedIndex].textContent.trim()
          : "";
      var whenLine = formatDateLong(String(dateIso)) + " at " + timeLabel;

      var lines = [
        "Reservation request — Zona Restaurant",
        "",
        "Date & time: " + whenLine,
        "Party size: " + (fd.get("party") || ""),
        "Name: " + (fd.get("name") || ""),
        "Email: " + (fd.get("email") || ""),
        "Phone: " + (fd.get("phone") || ""),
        "Comments: " + (fd.get("comments") || ""),
        "",
        "Please call (516) 799-4444 to confirm your table.",
      ];
      var text = lines.join("\n");

      function done() {
        statusEl.textContent =
          "Thank you. Your request summary was copied to the clipboard. Please call (516) 799-4444 to confirm your table.";
        form.reset();
        setReservationDateBounds();
        if (dateInput) dateInput.value = dateInput.min;
        refillTimeOptions();
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(done);
      } else {
        done();
      }
    });
  }

  var backTop = document.getElementById("back-to-top");
  window.addEventListener(
    "scroll",
    function () {
      if (!backTop) return;
      if (window.scrollY > 420) backTop.classList.add("is-visible");
      else backTop.classList.remove("is-visible");
    },
    { passive: true }
  );

  function syncMenuFromHash() {
    if (location.hash === "#catering") {
      openMenuPanel("catering");
    }
  }

  syncMenuFromHash();
  window.addEventListener("hashchange", syncMenuFromHash);
})();
