document.documentElement.classList.remove("no-js");

const root = document.documentElement;
const themeButton = document.querySelector("[data-theme-toggle]");
const storedTheme = localStorage.getItem("srms-theme");

if (storedTheme === "light" || storedTheme === "dark") {
  root.dataset.theme = storedTheme;
}

function updateThemeButton() {
  if (!themeButton) return;
  const isLight = root.dataset.theme === "light";
  themeButton.setAttribute(
    "aria-label",
    isLight ? "Switch to dark theme" : "Switch to light theme"
  );
  themeButton.setAttribute("title", isLight ? "Dark theme" : "Light theme");
}

updateThemeButton();

themeButton?.addEventListener("click", () => {
  const next = root.dataset.theme === "light" ? "dark" : "light";
  root.dataset.theme = next;
  localStorage.setItem("srms-theme", next);
  updateThemeButton();
});

const navToggle = document.querySelector("[data-nav-toggle]");
const navLinks = document.querySelector("[data-nav-links]");

navToggle?.addEventListener("click", () => {
  const open = navLinks?.classList.toggle("is-open");
  navToggle.setAttribute("aria-expanded", String(Boolean(open)));
});

navLinks?.addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    navLinks.classList.remove("is-open");
    navToggle?.setAttribute("aria-expanded", "false");
  }
});

document.addEventListener("click", (event) => {
  if (!navLinks?.classList.contains("is-open")) return;
  if (event.target.closest(".nav")) return;
  navLinks.classList.remove("is-open");
  navToggle?.setAttribute("aria-expanded", "false");
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && navLinks?.classList.contains("is-open")) {
    navLinks.classList.remove("is-open");
    navToggle?.setAttribute("aria-expanded", "false");
    navToggle?.focus();
  }
});

const header = document.querySelector("[data-header]");
const setHeaderState = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 12);
};
setHeaderState();
window.addEventListener("scroll", setHeaderState, { passive: true });

const setupTabs = (group) => {
  const tabs = [...group.querySelectorAll('[role="tab"]')];
  const panels = [...group.querySelectorAll('[role="tabpanel"]')];
  if (!tabs.length || !panels.length) return;

  const activate = (tab) => {
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute("aria-selected", String(selected));
      item.tabIndex = selected ? 0 : -1;
      item.classList.toggle("is-active", selected);
    });
    panels.forEach((panel) => {
      panel.hidden = panel.id !== tab.getAttribute("aria-controls");
    });
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(tab));
    tab.addEventListener("keydown", (event) => {
      let targetIndex = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") {
        targetIndex = (index + 1) % tabs.length;
      } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
        targetIndex = (index - 1 + tabs.length) % tabs.length;
      } else if (event.key === "Home") {
        targetIndex = 0;
      } else if (event.key === "End") {
        targetIndex = tabs.length - 1;
      } else {
        return;
      }
      event.preventDefault();
      tabs[targetIndex].focus();
      activate(tabs[targetIndex]);
    });
  });

  const initial = tabs.find((tab) => tab.getAttribute("aria-selected") === "true") || tabs[0];
  activate(initial);
};

document.querySelectorAll("[data-tabs]").forEach(setupTabs);

const copyText = async (text) => {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const area = document.createElement("textarea");
  area.value = text;
  area.style.position = "fixed";
  area.style.opacity = "0";
  document.body.appendChild(area);
  area.select();
  document.execCommand("copy");
  area.remove();
};

document.querySelectorAll(".code-shell").forEach((shell) => {
  const pre = shell.querySelector("pre");
  if (!pre) return;
  const head = shell.querySelector(".code-head");
  if (!head) return;
  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy-button";
  button.textContent = "Copy";
  head.appendChild(button);
  button.addEventListener("click", async () => {
    try {
      await copyText(pre.innerText);
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    } catch {
      button.textContent = "Press Ctrl+C";
    }
  });
});

const revealItems = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && revealItems.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -30px 0px" }
  );
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = String(new Date().getFullYear());
});

document.querySelectorAll("[data-copy-command]").forEach((button) => {
  button.addEventListener("click", async () => {
    const value = button.getAttribute("data-copy-command");
    if (!value) return;
    const original = button.textContent;
    try {
      await copyText(value);
      button.textContent = "Copied";
    } catch {
      button.textContent = "Copy failed";
    }
    setTimeout(() => {
      button.textContent = original;
    }, 1600);
  });
});
