import { getDictionary } from "@/i18n/server";

const ORDER = ["learn", "help", "check", "report"] as const;

const ICONS = {
  learn: (
    <>
      <path d="M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2V5z" />
      <path d="M8 7h6" />
    </>
  ),
  help: <path d="M4 5h16v11H9l-5 4V5z" />,
  check: (
    <>
      <circle cx="11" cy="11" r="6" />
      <path d="m16 16 5 5" />
    </>
  ),
  report: (
    <>
      <path d="M5 21V4" />
      <path d="M5 4h12l-2 4 2 4H5" />
    </>
  ),
};

export default async function Features() {
  const { t } = await getDictionary();

  return (
    <section id="what" className="scroll-mt-24 relative bg-[#d8e1eb] dark:bg-[#001433] px-6 py-28 overflow-hidden transition-colors duration-300">
      {/* Background ambient cosmic glow (dark theme only) */}
      <div
        aria-hidden="true"
        className="hidden dark:block pointer-events-none absolute -right-32 top-1/4 size-[26rem] rounded-full bg-brand-blue/15 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="hidden dark:block pointer-events-none absolute -left-32 bottom-10 size-80 rounded-full bg-brand-lime/10 blur-3xl"
      />

      <div className="relative z-10 mx-auto max-w-6xl">
        <h2 className="font-display text-3xl font-extrabold text-slate-900 dark:text-white sm:text-4xl lg:text-[2.75rem] tracking-tight">
          {t.what.title}
        </h2>
        <ul className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {ORDER.map((key, i) => (
            <li
              key={key}
              className="group relative rounded-[3px] border border-slate-200/90 bg-white p-6 shadow-sm transition-all duration-500 hover:-translate-y-1.5 hover:border-brand-blue/50 hover:shadow-md dark:border-white/10 dark:bg-white/[0.03] dark:shadow-none dark:backdrop-blur-xl dark:hover:border-brand-lime/50 dark:hover:bg-white/[0.06] dark:hover:shadow-[0_15px_40px_-10px_rgba(77,184,20,0.25)]"
            >
              <div
                className={`grid size-12 place-items-center rounded-[3px] border transition-all duration-300 group-hover:scale-105 ${
                  i % 2 === 0
                    ? "border-[#0066ff]/30 bg-[#0066ff]/10 text-[#0066ff] shadow-sm dark:border-brand-blue/30 dark:bg-brand-blue/15 dark:text-brand-blue dark:shadow-[0_0_20px_rgba(0,102,255,0.3)] dark:group-hover:shadow-[0_0_30px_rgba(0,102,255,0.5)]"
                    : "border-[#0066ff]/30 bg-[#0066ff]/10 text-[#0066ff] shadow-sm dark:border-brand-lime/30 dark:bg-brand-lime/15 dark:text-brand-lime dark:shadow-[0_0_20px_rgba(77,184,20,0.3)] dark:group-hover:shadow-[0_0_30px_rgba(77,184,20,0.5)]"
                }`}
              >
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
                  {ICONS[key]}
                </svg>
              </div>
              <h3 className="mt-5 font-display text-xl font-bold text-slate-900 dark:text-white tracking-tight group-hover:text-brand-blue dark:group-hover:text-brand-lime transition-colors duration-300">
                {t.what.cards[key].title}
              </h3>
              <p className="mt-2 text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300">
                {t.what.cards[key].body}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
