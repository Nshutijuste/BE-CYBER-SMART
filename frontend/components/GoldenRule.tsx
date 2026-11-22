import { getDictionary } from "@/i18n/server";

export default async function GoldenRule() {
  const { t } = await getDictionary();

  return (
    <section id="rule" className="relative bg-[#000714] px-6 py-24 overflow-hidden">
      <div className="relative z-10 mx-auto max-w-4xl">
        <div className="relative overflow-hidden rounded-3xl border border-brand-lime/40 bg-gradient-to-br from-[#001033]/90 via-[#000d26]/90 to-[#000714]/90 p-8 sm:p-12 md:p-16 shadow-[0_0_60px_rgba(77,184,20,0.2)] backdrop-blur-2xl">
          {/* Subtle neon corner accent */}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -right-20 -top-20 size-48 rounded-full bg-brand-lime/20 blur-2xl"
          />

          <div className="inline-flex size-14 items-center justify-center rounded-2xl border border-brand-lime/30 bg-brand-lime/10 text-brand-lime shadow-[0_0_30px_rgba(77,184,20,0.3)] mb-6">
            <svg
              viewBox="0 0 24 24"
              className="size-7"
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

          <h2 className="font-display text-3xl font-extrabold leading-tight text-white md:text-4xl">
            {t.rule.title}
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-slate-200 md:text-xl">
            {t.rule.body}
          </p>
        </div>
      </div>
    </section>
  );
}
