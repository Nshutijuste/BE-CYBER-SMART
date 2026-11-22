"use client";

import { useEffect, useRef, useState, useTransition } from "react";
import { setLocale } from "@/app/actions";
import Flag from "@/components/Flag";
import { locales, type Locale } from "@/i18n/config";

const short: Record<Locale, string> = { en: "EN", rw: "RW", fr: "FR" };
const names: Record<Locale, string> = {
  en: "English",
  rw: "Kinyarwanda",
  fr: "Français",
};

export default function LanguageMenu({
  current,
  label,
}: {
  current: Locale;
  label: string;
}) {
  const [open, setOpen] = useState(false);
  const [pending, startTransition] = useTransition();
  const root = useRef<HTMLDivElement>(null);
  const button = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    const outside = (e: Event) => {
      if (!root.current?.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        button.current?.focus();
      }
    };
    document.addEventListener("pointerdown", outside);
    document.addEventListener("focusin", outside);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", outside);
      document.removeEventListener("focusin", outside);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  function choose(l: Locale) {
    setOpen(false);
    startTransition(async () => {
      await setLocale(l);
    });
  }

  return (
    <div ref={root} className="group relative">
      <button
        ref={button}
        type="button"
        aria-label={label}
        aria-haspopup="true"
        aria-expanded={open}
        aria-controls="language-list"
        disabled={pending}
        onClick={() => setOpen(!open)}
        className="inline-flex h-9 sm:h-10 items-center gap-1.5 sm:gap-2 rounded-[2px] border border-slate-300/80 bg-white/80 dark:border-white/30 dark:bg-white/5 px-2.5 sm:px-3 text-xs sm:text-sm font-medium text-slate-800 dark:text-white hover:bg-slate-100 dark:hover:bg-white/15 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-lime"
      >
        <Flag locale={current} />
        <svg
          viewBox="0 0 12 12"
          className={`size-3 transition-transform ${open ? "rotate-180" : ""}`}
          aria-hidden="true"
        >
          <path
            d="M2 4l4 4 4-4"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {!open && (
        <span
          aria-hidden="true"
          className="pointer-events-none absolute right-0 top-full z-30 mt-2 hidden whitespace-nowrap rounded-[2px] bg-slate-900 px-3 py-1.5 text-xs font-medium text-white shadow-lg group-hover:block"
        >
          {label}
        </span>
      )}

      {open && (
        <ul
          id="language-list"
          className="absolute right-0 top-full z-30 mt-2 w-max overflow-hidden rounded-[2px] border border-slate-200 bg-white/95 text-slate-900 dark:border-white/15 dark:bg-[#000e24]/95 dark:text-white p-1.5 shadow-2xl backdrop-blur-xl ring-1 ring-black/5 dark:ring-white/10"
        >
          {locales
            .filter((l) => l !== current)
            .map((l) => (
              <li key={l}>
                <button
                  type="button"
                  lang={l}
                  title={names[l]}
                  onClick={() => choose(l)}
                  className="flex w-full items-center gap-2.5 rounded-[2px] px-3.5 py-2 text-left text-sm font-semibold text-slate-700 hover:bg-slate-100 hover:text-brand-blue dark:text-slate-200 dark:hover:bg-white/10 dark:hover:text-white transition-colors focus-visible:outline-2 focus-visible:outline-brand-lime"
                >
                  <Flag locale={l} />
                  <span aria-hidden="true">{short[l]}</span>
                  <span className="sr-only">{names[l]}</span>
                </button>
              </li>
            ))}
        </ul>
      )}
    </div>
  );
}