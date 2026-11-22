import { getDictionary } from "@/i18n/server";

export default async function GoldenRule() {
  const { t } = await getDictionary();

  return (
    <section id="rule" className="scroll-mt-24 relative bg-white dark:bg-[#001433] px-6 py-24 overflow-hidden transition-colors duration-300">
      <div className="relative z-10 mx-auto max-w-4xl">
        <div className="relative overflow-hidden rounded-[3px] border border-[#004181]/30 bg-[#d8e1eb]/70 p-6 sm:p-10 md:p-12 shadow-lg dark:border-blue-300/30 dark:bg-gradient-to-br dark:from-[#0a326c]/90 dark:via-[#0e3b7e]/90 dark:to-[#0b2b5c]/90 dark:shadow-[0_20px_50px_-10px_rgba(0,0,0,0.7),inset_0_1px_0_0_rgba(255,255,255,0.18)] backdrop-blur-2xl transition-all duration-300">
          {/* Subtle neon corner accent (dark theme only) */}
          <div
            aria-hidden="true"
            className="hidden dark:block pointer-events-none absolute -right-20 -top-20 size-48 rounded-full dark:bg-brand-lime/20 blur-2xl"
          />

          <div className="inline-flex size-12 items-center justify-center rounded-[3px] border border-[#004181]/40 bg-[#004181]/15 text-[#004181] dark:border-brand-lime/30 dark:bg-brand-lime/10 dark:text-brand-lime shadow-sm dark:shadow-[0_0_20px_rgba(77,184,20,0.3)] mb-5">
            <svg
              viewBox="0 0 24 24"
              className="size-6"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>

          <h2 className="font-display text-3xl font-bold leading-tight text-slate-900 dark:text-white sm:text-4xl">
            {t.rule.title}
          </h2>
          <p className="mt-4 text-[17px] sm:text-[19px] leading-relaxed text-slate-700 dark:text-slate-200">
            {t.rule.body}
          </p>
        </div>
      </div>
    </section>
  );
}
