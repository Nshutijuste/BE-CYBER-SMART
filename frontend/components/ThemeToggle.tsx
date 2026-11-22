"use client";

import { useSyncExternalStore } from "react";

function subscribe(callback: () => void) {
  const observer = new MutationObserver(callback);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class", "data-theme"],
  });
  window.addEventListener("storage", callback);
  return () => {
    observer.disconnect();
    window.removeEventListener("storage", callback);
  };
}

function getSnapshot(): "dark" | "light" {
  if (typeof document === "undefined") return "dark";
  const isLight = document.documentElement.classList.contains("light");
  return isLight ? "light" : "dark";
}

function getServerSnapshot(): "dark" | "light" {
  return "dark";
}

export default function ThemeToggle() {
  const theme = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  function toggleTheme() {
    const nextTheme = theme === "dark" ? "light" : "dark";
    try {
      localStorage.setItem("theme", nextTheme);
    } catch {
      // ignore
    }

    if (nextTheme === "dark") {
      document.documentElement.classList.add("dark");
      document.documentElement.classList.remove("light");
      document.documentElement.dataset.theme = "dark";
    } else {
      document.documentElement.classList.remove("dark");
      document.documentElement.classList.add("light");
      document.documentElement.dataset.theme = "light";
    }
  }

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={
        theme === "dark" ? "Switch to Light mode" : "Switch to Dark mode"
      }
      title={
        theme === "dark" ? "Switch to Light mode" : "Switch to Dark mode"
      }
      className="inline-flex h-9 sm:h-10 items-center justify-center gap-1.5 rounded-[3px] border border-slate-300/80 bg-white/80 px-2.5 text-xs font-semibold text-slate-800 shadow-sm transition-colors hover:bg-white dark:border-white/20 dark:bg-white/5 dark:text-slate-200 dark:hover:bg-white/15 dark:shadow-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-lime"
    >
      {theme === "dark" ? (
        <>
          {/* Sun icon for switching to light mode */}
          <svg
            viewBox="0 0 24 24"
            className="size-4 text-amber-400"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
          </svg>
          <span className="hidden xl:inline text-xs">Light</span>
        </>
      ) : (
        <>
          {/* Moon icon for switching to dark mode */}
          <svg
            viewBox="0 0 24 24"
            className="size-4 text-brand-blue"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
          </svg>
          <span className="hidden xl:inline text-xs">Dark</span>
        </>
      )}
    </button>
  );
}
