import type { ReactNode } from "react";
import type { Locale } from "@/i18n/config";

const flags: Record<Locale, ReactNode> = {
  en: (
    <g transform="scale(1 1.3333)">
      <rect width="60" height="30" fill="#012169" />
      <path d="M-5 -2.5 L65 32.5 M65 -2.5 L-5 32.5" stroke="#fff" strokeWidth="6" />
      <path d="M-5 -2.5 L65 32.5 M65 -2.5 L-5 32.5" stroke="#C8102E" strokeWidth="2.4" />
      <path d="M30 0 V30 M0 15 H60" stroke="#fff" strokeWidth="10" />
      <path d="M30 0 V30 M0 15 H60" stroke="#C8102E" strokeWidth="6" />
    </g>
  ),
  rw: (
    <>
      <rect width="60" height="20" fill="#00A1DE" />
      <rect y="20" width="60" height="10" fill="#FAD201" />
      <rect y="30" width="60" height="10" fill="#20603D" />
      <circle cx="47" cy="10" r="4.2" fill="#FAD201" />
      <circle
        cx="47"
        cy="10"
        r="6.6"
        fill="none"
        stroke="#FAD201"
        strokeWidth="2.6"
        strokeDasharray="1.6 1.7"
      />
    </>
  ),
  fr: (
    <>
      <rect width="20" height="40" fill="#0055A4" />
      <rect x="20" width="20" height="40" fill="#ffffff" />
      <rect x="40" width="20" height="40" fill="#EF4135" />
    </>
  ),
};

export default function Flag({ locale }: { locale: Locale }) {
  return (
    <svg
      viewBox="0 0 60 40"
      className="h-4 w-6 shrink-0 rounded-[3px] ring-1 ring-black/25"
      aria-hidden="true"
    >
      {flags[locale]}
    </svg>
  );
}