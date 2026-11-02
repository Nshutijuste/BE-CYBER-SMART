"use client";

import { useTransition } from "react";
import { setLocale } from "@/app/actions";
import { locales, type Locale } from "@/i18n/config";

const short: Record<Locale, string> = { en: "EN", rw: "RW" };
const full: Record<Locale, string> = { en: "English", rw: "Kinyarwanda" };

export default function LanguageSwitch({
  current,
  label,
}: {
  current: Locale;
  label: string;
}) {
  const [pending, startTransition] = useTransition();

  return (
    <div
      role="group"
      aria-label={label}
      className="inline-flex overflow-hidden rounded-lg border border-brand-navy/30 text-sm font-semibold"
    >
      {locales.map((l) => (
        <button
          key={l}
          type="button"
          lang={l}
          title={full[l]}
          aria-pressed={l === current}
          disabled={pending}
          onClick={() =>
            startTransition(async () => {
              await setLocale(l);
            })
          }
          className={`px-3 py-1.5 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-blue ${
            l === current
              ? "bg-brand-navy text-white"
              : "text-brand-navy hover:bg-brand-navy/10"
          }`}
        >
          {short[l]}
        </button>
      ))}
    </div>
  );
}