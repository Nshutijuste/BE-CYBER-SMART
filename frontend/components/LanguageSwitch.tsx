"use client";

import { useTransition } from "react";
import { setLocale } from "@/app/actions";
import { locales, type Locale } from "@/i18n/config";

const short: Record<Locale, string> = { en: "EN", rw: "RW" };
const full: Record<Locale, string> = { en: "English", rw: "Kinyarwanda" };

export default function LanguageSwitch({
  current,
  label,
  onDark = false,
}: {
  current: Locale;
  label: string;
  onDark?: boolean;
}) {
  const [pending, startTransition] = useTransition();

  return (
    <div
      role="group"
      aria-label={label}
      className={`inline-flex overflow-hidden rounded-lg border text-base font-semibold ${
        onDark ? "border-white/50" : "border-brand-navy/30"
      }`}
    >
      {locales.map((l) => {
        const active = l === current;
        const tone = onDark
          ? active
            ? "bg-white text-brand-navy"
            : "text-white hover:bg-white/15"
          : active
            ? "bg-brand-navy text-white"
            : "text-brand-navy hover:bg-brand-navy/10";
        const ring = onDark ? "focus-visible:outline-brand-lime" : "focus-visible:outline-brand-blue";
        return (
          <button
            key={l}
            type="button"
            lang={l}
            title={full[l]}
            aria-pressed={active}
            disabled={pending}
            onClick={() =>
              startTransition(async () => {
                await setLocale(l);
              })
            }
            className={`px-3.5 py-2 focus-visible:outline-2 focus-visible:-outline-offset-2 ${ring} ${tone}`}
          >
            {short[l]}
          </button>
        );
      })}
    </div>
  );
}