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
    <section id="what" className="relative bg-[#000714] px-6 py-28 overflow-hidden">
      {/* Background ambient cosmic glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 top-1/4 size-[26rem] rounded-full bg-brand-blue/15 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -left-32 bottom-10 size-80 rounded-full bg-brand-lime/10 blur-3xl"
      />

      <div className="relative z-10 mx-auto max-w-6xl">
        <div className="inline-flex items-center gap-2 rounded-full border border-brand-lime/30 bg-brand-lime/10 px-3.5 py-1 text-xs font-bold uppercase tracking-wider text-brand-lime mb-3">
          Core Capabilities
        </div>
        <h2 className="font-display text-3xl font-extrabold text-white md:text-5xl tracking-tight">
          {t.what.title}
        </h2>
        <ul className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {ORDER.map((key, i) => (
            <li
              key={key}
              className="group relative rounded-3xl border border-white/10 bg-white/[0.03] p-7 backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-brand-lime/50 hover:bg-white/[0.06] hover:shadow-[0_15px_40px_-10px_rgba(77,184,20,0.25)]"
            >
              <div
                className={`grid size-14 place-items-center rounded-2xl border transition-all duration-300 group-hover:scale-110 ${
                  i % 2 === 0
                    ? "border-brand-blue/30 bg-brand-blue/15 text-brand-blue shadow-[0_0_20px_rgba(0,102,255,0.3)] group-hover:shadow-[0_0_30px_rgba(0,102,255,0.5)]"
                    : "border-brand-lime/30 bg-brand-lime/15 text-brand-lime shadow-[0_0_20px_rgba(77,184,20,0.3)] group-hover:shadow-[0_0_30px_rgba(77,184,20,0.5)]"
                }`}
              >
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
                  {ICONS[key]}
                </svg>
              </div>
              <h3 className="mt-6 font-display text-2xl font-bold text-white tracking-tight group-hover:text-brand-lime transition-colors duration-300">
                {t.what.cards[key].title}
              </h3>
              <p className="mt-3 text-base leading-relaxed text-slate-300">
                {t.what.cards[key].body}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
