"use client";

import { useEffect, useState } from "react";
import LanguageSwitch from "@/components/LanguageSwitch";
import type { Locale } from "@/i18n/config";

type NavLink = { href: string; label: string };

export default function MobileMenu({
  links,
  label,
  locale,
  languageLabel,
}: {
  links: NavLink[];
  label: string;
  locale: Locale;
  languageLabel: string;
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
        aria-expanded={open}
        aria-controls="mobile-menu"
        onClick={() => setOpen(!open)}
        className="rounded-lg border border-white/50 px-4 py-2 text-base font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-lime"
      >
        {label}
      </button>
      {open && (
        <div
          id="mobile-menu"
          className="absolute inset-x-4 top-full z-20 mt-1 rounded-2xl bg-white p-3 shadow-xl"
        >
          <nav aria-label={label}>
            <ul>
              {links.map((l) => (
                <li key={l.href}>
                  <a
                    href={l.href}
                    onClick={() => setOpen(false)}
                    className="block rounded-lg px-4 py-3 text-lg font-semibold text-brand-navy hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-brand-blue"
                  >
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
          <div className="mt-2 border-t border-slate-200 px-4 pb-2 pt-4">
            <p className="mb-2 text-sm font-semibold text-slate-600">{languageLabel}</p>
            <LanguageSwitch current={locale} label={languageLabel} />
          </div>
        </div>
      )}
    </div>
  );
}