"use client";

import { useEffect, useState } from "react";

type NavLink = { href: string; label: string };

export default function MobileMenu({
  links,
  label,
}: {
  links: NavLink[];
  label: string;
}) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <div className="lg:hidden">
      <button
        type="button"
        aria-label={label}
        aria-expanded={open}
        aria-controls="mobile-menu"
        onClick={() => setOpen(!open)}
        className="inline-flex h-9 sm:h-10 items-center gap-1.5 sm:gap-2 rounded-[2px] border border-slate-300/80 bg-white/80 dark:border-white/30 dark:bg-white/5 px-2.5 sm:px-3 text-xs sm:text-sm font-medium text-slate-800 dark:text-white hover:bg-slate-100 dark:hover:bg-white/15 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-lime"
      >
        <svg
          viewBox="0 0 24 24"
          className="size-5"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          aria-hidden="true"
        >
          {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
        </svg>
        <span className="hidden sm:inline">{label}</span>
      </button>
      {open && (
        <nav
          id="mobile-menu"
          aria-label={label}
          className="absolute inset-x-4 top-full z-20 mt-2 rounded-[2px] border border-slate-200 bg-white/95 text-slate-900 dark:border-white/15 dark:bg-[#000e24]/95 dark:text-white p-2 shadow-2xl backdrop-blur-xl"
        >
          <ul>
            {links.map((l) => (
              <li key={l.href}>
                <a
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="block rounded-[2px] px-4 py-2.5 text-base font-semibold text-slate-700 hover:bg-slate-100 hover:text-brand-blue dark:text-slate-200 dark:hover:bg-white/10 dark:hover:text-brand-lime transition-colors focus-visible:outline-2 focus-visible:outline-brand-lime"
                >
                  {l.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
}