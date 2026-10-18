(() => {
  "use strict";

  const start = () => {
    const doc = document;
    const root = doc.documentElement;
    root.classList.add("js-ready");
    const urlParameters = new URLSearchParams(window.location.search);
    const isTurkish = doc.body.dataset.lang === "tr" || root.lang === "tr";
    const locale = isTurkish ? "tr-TR" : "en-GB";
    const text = {
      copied: isTurkish ? "Panoya kopyalandı." : "Copied to clipboard.",
      copyFailed: isTurkish
        ? "Kopyalanamadı. Lütfen metni seçip kopyalayın."
        : "Could not copy. Please select and copy the text.",
      lightTheme: isTurkish ? "Açık temaya geç" : "Switch to light theme",
      darkTheme: isTurkish ? "Koyu temaya geç" : "Switch to dark theme",
      emailDraft: isTurkish
        ? "E-posta uygulamanızda bir taslak açılıyor."
        : "Opening a draft in your email app.",
      noRecipient: isTurkish
        ? "Lütfen sayfadaki e-posta bağlantısını kullanın."
        : "Please use the email link on this page.",
    };
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const normalize = (value) =>
      String(value || "")
        .toLocaleLowerCase("tr-TR")
        .replace(/ı/g, "i")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
    const matches = (haystack, query) =>
      normalize(query)
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .every((word) => normalize(haystack).includes(word));
    const closest = (event, selector) =>
      event.target instanceof Element ? event.target.closest(selector) : null;
    const listenForMotion = (callback) => {
      if (reducedMotion.addEventListener) reducedMotion.addEventListener("change", callback);
      else if (reducedMotion.addListener) reducedMotion.addListener(callback);
    };

    let toastTimer;
    const toast = (message) => {
      const status = doc.querySelector("[data-toast]");
      if (!status) return;
      clearTimeout(toastTimer);
      status.hidden = false;
      status.textContent = message;
      status.classList.add("is-visible");
      toastTimer = window.setTimeout(() => {
        status.classList.remove("is-visible");
        status.hidden = true;
      }, 3400);
    };

    const legacyCopy = (value) => {
      const previousFocus = doc.activeElement;
      const input = doc.createElement("textarea");
      input.value = value;
      input.setAttribute("readonly", "");
      input.style.cssText = "position:fixed;inset:0 auto auto 0;opacity:0;pointer-events:none;";
      // A textarea in an open modal must be inside the dialog to receive focus.
      const modal = doc.querySelector("dialog[open]");
      (modal || doc.body).append(input);
      input.select();
      input.setSelectionRange(0, value.length);
      let success = false;
      try {
        success = doc.execCommand("copy");
      } catch (_) {
        /* Use the visible fallback message. */
      }
      input.remove();
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) {
        previousFocus.focus({ preventScroll: true });
      }
      return success;
    };
    const copy = async (value) => {
      if (!value) return;
      let success = false;
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(value);
          success = true;
        }
      } catch (_) {
        /* Some browsers require the legacy user-gesture fallback. */
      }
      if (!success) success = legacyCopy(value);
      toast(success ? text.copied : text.copyFailed);
    };

    const updateThemeControls = () => {
      const dark = root.dataset.theme !== "light";
      doc.querySelectorAll("[data-theme-toggle]").forEach((button) => {
        button.setAttribute("aria-label", dark ? text.lightTheme : text.darkTheme);
        button.setAttribute("title", dark ? text.lightTheme : text.darkTheme);
        button.setAttribute("aria-pressed", String(dark));
        const label = button.querySelector("[data-theme-label]");
        if (label) label.textContent = dark ? text.lightTheme : text.darkTheme;
      });
    };
    updateThemeControls();
    doc.addEventListener("click", (event) => {
      const themeButton = closest(event, "[data-theme-toggle]");
      if (themeButton) {
        event.preventDefault();
        root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
        try {
          localStorage.setItem("macakr-theme", root.dataset.theme);
        } catch (_) {
          /* Private storage is optional. */
        }
        updateThemeControls();
        doc.dispatchEvent(
          new CustomEvent("portfolio:theme", { detail: { theme: root.dataset.theme } }),
        );
      }
      const copyButton = closest(event, "[data-copy]");
      if (copyButton) {
        event.preventDefault();
        void copy(copyButton.dataset.copy || "");
      }
      const codeButton = closest(event, "[data-copy-code]");
      if (codeButton) {
        event.preventDefault();
        let code;
        try {
          code = doc.querySelector(codeButton.dataset.copyCode);
        } catch (_) {
          /* Ignore invalid selectors. */
        }
        if (code) void copy(code.textContent || "");
      }
      if (closest(event, "[data-print]")) {
        event.preventDefault();
        window.print();
      }
    });

    // The navigation stays usable in the document when JavaScript is unavailable.
    const menuButton = doc.querySelector("[data-menu-toggle]");
    const sidebar = doc.querySelector(".sidebar");
    const backdrop = doc.querySelector("[data-menu-backdrop]");
    const desktopMenu = window.matchMedia("(min-width: 961px)");
    let menuOpen = false;
    const setMenu = (open, returnFocus = false) => {
      menuOpen = Boolean(open && !desktopMenu.matches);
      doc.body.classList.toggle("menu-open", menuOpen);
      if (sidebar) {
        const inaccessible = !desktopMenu.matches && !menuOpen;
        sidebar.classList.toggle("is-open", menuOpen);
        sidebar.inert = inaccessible;
        if (inaccessible) sidebar.setAttribute("aria-hidden", "true");
        else sidebar.removeAttribute("aria-hidden");
      }
      if (menuButton) menuButton.setAttribute("aria-expanded", String(menuOpen));
      if (backdrop) backdrop.hidden = !menuOpen;
      if (returnFocus && menuButton) menuButton.focus({ preventScroll: true });
    };
    if (menuButton) menuButton.addEventListener("click", () => setMenu(!menuOpen));
    if (backdrop) backdrop.addEventListener("click", () => setMenu(false, true));
    if (sidebar)
      sidebar.addEventListener("click", (event) => {
        if (closest(event, "a[href]") && menuOpen) setMenu(false);
      });
    const handleMenuViewport = () => {
      const returnFocus = !desktopMenu.matches && !menuOpen && sidebar?.contains(doc.activeElement);
      setMenu(menuOpen, returnFocus);
    };
    if (desktopMenu.addEventListener) desktopMenu.addEventListener("change", handleMenuViewport);
    else if (desktopMenu.addListener) desktopMenu.addListener(handleMenuViewport);
    setMenu(false);

    const palette = doc.querySelector("#command-palette");
    let closePalette = () => {};
    let revealFilteredTarget = () => {};
    if (palette instanceof HTMLDialogElement) {
      const search = palette.querySelector("[data-command-search]");
      const list = palette.querySelector("[data-command-list]");
      const commands = Array.from(palette.querySelectorAll("[data-command-item]"));
      const empty = palette.querySelector("[data-command-empty]");
      let paletteTrigger;
      let backdropPointerDown = false;
      const visibleCommands = () => commands.filter((command) => !command.hidden);
      const clearCommandSelection = () =>
        commands.forEach((command) => command.classList.remove("is-active"));
      const filterCommands = () => {
        const query = search ? search.value : "";
        commands.forEach((command) => {
          command.hidden = !matches(
            `${command.dataset.search || ""} ${command.textContent || ""}`,
            query,
          );
        });
        clearCommandSelection();
        if (empty) empty.hidden = visibleCommands().length > 0;
        if (list) list.scrollTop = 0;
      };
      const openPalette = (trigger) => {
        if (palette.open) return;
        paletteTrigger = trigger instanceof HTMLElement ? trigger : doc.activeElement;
        if (menuOpen) {
          if (sidebar && sidebar.contains(paletteTrigger)) paletteTrigger = menuButton;
          setMenu(false);
        }
        if (search) search.value = "";
        filterCommands();
        palette.showModal();
        doc.body.classList.add("command-open");
        if (search) search.focus({ preventScroll: true });
      };
      closePalette = () => {
        if (palette.open) palette.close();
      };
      palette.addEventListener("close", () => {
        doc.body.classList.remove("command-open");
        clearCommandSelection();
        const focusTarget = [
          paletteTrigger,
          menuButton,
          ...doc.querySelectorAll("[data-command-open]"),
        ].find(
          (element) =>
            element instanceof HTMLElement &&
            element.isConnected &&
            !element.closest("[inert]") &&
            element.getClientRects().length,
        );
        if (focusTarget) focusTarget.focus({ preventScroll: true });
      });
      doc.querySelectorAll("[data-command-open]").forEach((button) => {
        button.setAttribute("aria-haspopup", "dialog");
        button.setAttribute("aria-controls", palette.id);
        button.addEventListener("click", () => openPalette(button));
      });
      palette
        .querySelectorAll("[data-command-close]")
        .forEach((button) => button.addEventListener("click", closePalette));
      if (search) search.addEventListener("input", filterCommands);
      const outsideDialog = (event) => {
        const rect = palette.getBoundingClientRect();
        return (
          event.target === palette &&
          (event.clientX < rect.left ||
            event.clientX > rect.right ||
            event.clientY < rect.top ||
            event.clientY > rect.bottom)
        );
      };
      palette.addEventListener("pointerdown", (event) => {
        backdropPointerDown = outsideDialog(event);
      });
      palette.addEventListener("pointercancel", () => {
        backdropPointerDown = false;
      });
      palette.addEventListener("click", (event) => {
        if (backdropPointerDown && outsideDialog(event)) closePalette();
        backdropPointerDown = false;
        const command = closest(event, "[data-command-item]");
        if (command) {
          if (command instanceof HTMLAnchorElement) {
            const destination = new URL(command.href, window.location.href);
            if (
              destination.origin === window.location.origin &&
              destination.pathname === window.location.pathname &&
              destination.search === window.location.search
            ) {
              revealFilteredTarget(destination.hash);
            }
          }
          closePalette();
        }
      });
      palette.addEventListener("keydown", (event) => {
        const visible = visibleCommands();
        const current = visible.indexOf(doc.activeElement);
        let next;
        if (event.key === "ArrowDown") next = current < 0 ? 0 : (current + 1) % visible.length;
        if (event.key === "ArrowUp")
          next = current < 0 ? visible.length - 1 : (current - 1 + visible.length) % visible.length;
        if (event.key === "Home" && doc.activeElement !== search) next = 0;
        if (event.key === "End" && doc.activeElement !== search) next = visible.length - 1;
        if (next !== undefined && visible.length) {
          event.preventDefault();
          clearCommandSelection();
          visible[next].classList.add("is-active");
          visible[next].focus({ preventScroll: true });
          visible[next].scrollIntoView({ block: "nearest" });
        }
        if (event.key === "Enter" && doc.activeElement === search && visible.length) {
          event.preventDefault();
          visible[0].click();
        }
      });
      doc.addEventListener("keydown", (event) => {
        if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k" && !event.altKey) {
          event.preventDefault();
          if (palette.open) closePalette();
          else openPalette(doc.activeElement);
        }
      });
    }
    doc.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuOpen) {
        event.preventDefault();
        setMenu(false, true);
      }
      if (event.key === "Tab" && menuOpen && sidebar && menuButton) {
        const links = Array.from(
          sidebar.querySelectorAll(
            'a[href], button:not([disabled]), input:not([disabled]), [tabindex="0"]',
          ),
        ).filter((element) => !element.hidden && element.getClientRects().length > 0);
        const controls = [menuButton, ...links.filter((element) => element !== menuButton)];
        const current = controls.indexOf(doc.activeElement);
        const next =
          current < 0
            ? event.shiftKey
              ? controls.length - 1
              : 0
            : (current + (event.shiftKey ? -1 : 1) + controls.length) % controls.length;
        event.preventDefault();
        controls[next].focus();
      }
    });

    const grid = doc.querySelector("[data-filter-grid]");
    if (grid) {
      const items = Array.from(grid.querySelectorAll("[data-filter-item]"));
      const filters = Array.from(doc.querySelectorAll("[data-filter]"));
      const search = doc.querySelector("[data-filter-search]");
      const count = doc.querySelector("[data-filter-count]");
      const empty = doc.querySelector("[data-filter-empty]");
      const requestedCategory = urlParameters.get("category");
      let category = filters.some((button) => button.dataset.filter === requestedCategory)
        ? requestedCategory
        : (filters.find((button) => button.getAttribute("aria-pressed") === "true") || {}).dataset
            ?.filter || "all";
      const applyFilters = () => {
        const query = search ? search.value : "";
        let total = 0;
        items.forEach((item) => {
          const categories = normalize(item.dataset.category).split(/[\s,|]+/);
          const shown =
            (category === "all" || categories.includes(normalize(category))) &&
            matches(`${item.dataset.search || ""} ${item.textContent || ""}`, query);
          item.hidden = !shown;
          if (shown) total += 1;
        });
        filters.forEach((button) => {
          const active = button.dataset.filter === category;
          button.setAttribute("aria-pressed", String(active));
          button.classList.toggle("is-active", active);
        });
        if (count) count.textContent = new Intl.NumberFormat(locale).format(total);
        if (empty) empty.hidden = total !== 0;
      };
      filters.forEach((button) =>
        button.addEventListener("click", () => {
          category = button.dataset.filter || "all";
          applyFilters();
        }),
      );
      if (search) search.addEventListener("input", applyFilters);
      doc.querySelectorAll("[data-filter-reset]").forEach((button) =>
        button.addEventListener("click", () => {
          category = "all";
          if (search) search.value = "";
          applyFilters();
          if (search) search.focus({ preventScroll: true });
        }),
      );
      applyFilters();
      revealFilteredTarget = (hash) => {
        let id;
        try {
          id = decodeURIComponent((hash || "").replace(/^#/, ""));
        } catch (_) {
          return;
        }
        const target = id ? doc.getElementById(id) : null;
        if (!target || !grid.contains(target)) return;
        const item = target.closest("[data-filter-item]");
        if (item && item.hidden) {
          category = "all";
          if (search) search.value = "";
          applyFilters();
        }
      };
      revealFilteredTarget(window.location.hash);
      window.addEventListener("hashchange", () => revealFilteredTarget(window.location.hash));
    }

    const tabs = Array.from(doc.querySelectorAll("[data-tab]"));
    const tabPanels = Array.from(doc.querySelectorAll("[data-tab-panel]"));
    if (tabs.length && tabPanels.length) {
      const activateTab = (tab, focus = false) => {
        tabs.forEach((button) => {
          const selected = button === tab;
          button.setAttribute("aria-selected", String(selected));
          button.tabIndex = selected ? 0 : -1;
          button.classList.toggle("is-active", selected);
        });
        tabPanels.forEach((panel) => {
          panel.hidden = panel.dataset.tabPanel !== tab.dataset.tab;
        });
        if (focus) tab.focus({ preventScroll: true });
      };
      tabs.forEach((tab, index) => {
        tab.setAttribute("role", "tab");
        if (!tab.id) tab.id = `lab-tab-${index + 1}`;
        const panel = tabPanels.find((item) => item.dataset.tabPanel === tab.dataset.tab);
        if (panel) {
          if (!panel.id) panel.id = `lab-panel-${index + 1}`;
          tab.setAttribute("aria-controls", panel.id);
          panel.setAttribute("role", "tabpanel");
          panel.setAttribute("aria-labelledby", tab.id);
          panel.tabIndex = 0;
        }
        tab.addEventListener("click", () => activateTab(tab));
        tab.addEventListener("keydown", (event) => {
          let next;
          if (event.key === "ArrowRight" || event.key === "ArrowDown")
            next = (index + 1) % tabs.length;
          if (event.key === "ArrowLeft" || event.key === "ArrowUp")
            next = (index - 1 + tabs.length) % tabs.length;
          if (event.key === "Home") next = 0;
          if (event.key === "End") next = tabs.length - 1;
          if (next !== undefined) {
            event.preventDefault();
            activateTab(tabs[next], true);
          }
        });
      });
      if (tabs.every((tab) => tab.parentElement === tabs[0].parentElement))
        tabs[0].parentElement.setAttribute("role", "tablist");
      const requestedTab = urlParameters.get("tab");
      activateTab(
        tabs.find((tab) => tab.dataset.tab === requestedTab) ||
          tabs.find((tab) => tab.getAttribute("aria-selected") === "true") ||
          tabs[0],
      );
    }

    doc.querySelectorAll("[data-model-viewer]").forEach((viewer) => {
      const model = viewer.querySelector("[data-model-rotate]");
      if (!model) return;
      const range = viewer.querySelector("[data-model-angle]");
      const reset = viewer.querySelector("[data-model-reset]");
      const auto = viewer.querySelector("[data-model-auto]");
      const initialAngle = range ? Number(range.defaultValue || range.value || 24) : 24;
      let angle = initialAngle;
      let tilt = -16;
      let autorotate = auto?.getAttribute("aria-pressed") === "true" && !reducedMotion.matches;
      let onScreen = true;
      let dragging = false;
      let pointer;
      let frame = 0;
      let lastTime = 0;
      const draw = () => {
        model.style.transform = `rotateX(${tilt}deg) rotateY(${angle}deg)`;
        model.style.setProperty("--model-angle", `${angle}deg`);
        if (range) range.value = String(((angle % 360) + 360) % 360);
      };
      const updateAuto = () => {
        if (!auto) return;
        auto.setAttribute("aria-pressed", String(autorotate));
        auto.disabled = reducedMotion.matches;
        const label = autorotate ? auto.dataset.stop : auto.dataset.start;
        if (label) auto.textContent = label;
      };
      const reconcileMotionPreference = () => {
        if (reducedMotion.matches) autorotate = false;
        updateAuto();
      };
      const shouldAnimate = () =>
        autorotate && !reducedMotion.matches && !doc.hidden && onScreen && !dragging;
      const tick = (timestamp) => {
        frame = 0;
        if (!shouldAnimate()) {
          // Keep controls truthful even if a browser coalesces the media change event.
          reconcileMotionPreference();
          lastTime = 0;
          return;
        }
        if (lastTime) angle += Math.min(timestamp - lastTime, 50) * 0.012;
        lastTime = timestamp;
        draw();
        frame = window.requestAnimationFrame(tick);
      };
      const syncAnimation = () => {
        reconcileMotionPreference();
        if (!shouldAnimate()) {
          if (frame) window.cancelAnimationFrame(frame);
          frame = 0;
          lastTime = 0;
        } else if (!frame) frame = window.requestAnimationFrame(tick);
      };
      if (range)
        range.addEventListener("input", () => {
          angle = Number(range.value);
          autorotate = false;
          updateAuto();
          syncAnimation();
          draw();
        });
      if (reset)
        reset.addEventListener("click", () => {
          angle = initialAngle;
          tilt = -16;
          autorotate = false;
          updateAuto();
          syncAnimation();
          draw();
        });
      if (auto)
        auto.addEventListener("click", () => {
          // An explicit press may enable movement, but never overrides reduced motion.
          autorotate = !autorotate && !reducedMotion.matches;
          updateAuto();
          syncAnimation();
        });
      model.style.touchAction = "pan-y";
      model.addEventListener("pointerdown", (event) => {
        if (event.button !== 0 || !event.isPrimary) return;
        dragging = true;
        pointer = { id: event.pointerId, x: event.clientX, y: event.clientY, angle, tilt };
        model.classList.add("is-dragging");
        try {
          model.setPointerCapture(event.pointerId);
        } catch (_) {
          /* Pointer capture is a progressive enhancement. */
        }
        syncAnimation();
      });
      model.addEventListener("pointermove", (event) => {
        if (!dragging || !pointer || event.pointerId !== pointer.id) return;
        angle = pointer.angle + (event.clientX - pointer.x) * 0.55;
        tilt = Math.max(-55, Math.min(55, pointer.tilt - (event.clientY - pointer.y) * 0.3));
        draw();
      });
      const stopDrag = (event) => {
        if (!pointer || event.pointerId !== pointer.id) return;
        dragging = false;
        pointer = null;
        model.classList.remove("is-dragging");
        syncAnimation();
      };
      model.addEventListener("pointerup", stopDrag);
      model.addEventListener("pointercancel", stopDrag);
      model.addEventListener("lostpointercapture", stopDrag);
      if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
          (entries) => {
            onScreen = entries[0].isIntersecting;
            syncAnimation();
          },
          { rootMargin: "80px" },
        );
        observer.observe(viewer);
      }
      doc.addEventListener("visibilitychange", syncAnimation);
      listenForMotion(() => {
        if (reducedMotion.matches) autorotate = false;
        updateAuto();
        syncAnimation();
      });
      updateAuto();
      draw();
      syncAnimation();
    });

    const placeButtons = Array.from(doc.querySelectorAll("[data-place]"));
    const placeCards = Array.from(doc.querySelectorAll("[data-place-card]"));
    const selectPlace = (selected) => {
      placeButtons.forEach((button) => {
        const active = button.dataset.place === selected;
        button.setAttribute("aria-pressed", String(active));
        button.classList.toggle("is-active", active);
      });
      placeCards.forEach((card) => {
        const active = card.dataset.placeCard === selected;
        card.classList.toggle("is-active", active);
        card.classList.toggle("is-selected", active);
      });
    };
    placeButtons.forEach((button) =>
      button.addEventListener("click", () => selectPlace(button.dataset.place)),
    );
    const initiallySelectedPlace = placeButtons.find(
      (button) => button.getAttribute("aria-pressed") === "true",
    );
    if (initiallySelectedPlace) selectPlace(initiallySelectedPlace.dataset.place);

    doc.querySelectorAll("[data-contact-form]").forEach((form) =>
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;
        const field = (name) => {
          const element = form.elements.namedItem(name);
          return element && "value" in element ? String(element.value).trim() : "";
        };
        const recipient = form.dataset.recipient || field("recipient");
        if (!recipient) {
          toast(text.noRecipient);
          return;
        }
        const sender = field("email");
        const name = field("name");
        const subject =
          field("subject") || (isTurkish ? "Web sitesinden iletişim" : "Portfolio enquiry");
        const message = field("message");
        const signature = [name, sender].filter(Boolean).join(" · ");
        const body = signature ? `${message}\n\n${signature}` : message;
        const mailto = `mailto:${encodeURIComponent(recipient)}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        window.location.href = mailto;
        toast(text.emailDraft);
      }),
    );

    const clocks = Array.from(doc.querySelectorAll("[data-clock]"));
    if (clocks.length) {
      const formatter = new Intl.DateTimeFormat(locale, {
        timeZone: "Europe/Istanbul",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      });
      const updateClock = () => {
        if (doc.hidden) return;
        const now = new Date();
        clocks.forEach((clock) => {
          clock.textContent = formatter.format(now);
          if (clock instanceof HTMLTimeElement) clock.dateTime = now.toISOString();
        });
      };
      updateClock();
      window.setInterval(updateClock, 15000);
      doc.addEventListener("visibilitychange", updateClock);
    }

    const revealElements = doc.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && !reducedMotion.matches) {
      const observer = new IntersectionObserver(
        (entries) =>
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }),
        { threshold: 0.08 },
      );
      revealElements.forEach((element) => observer.observe(element));
      listenForMotion(() => {
        if (reducedMotion.matches) {
          revealElements.forEach((element) => element.classList.add("is-visible"));
          observer.disconnect();
        }
      });
    } else revealElements.forEach((element) => element.classList.add("is-visible"));

    doc.body.classList.add("js-ready");
  };

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", start, { once: true });
  else start();
})();
