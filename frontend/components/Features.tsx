import { getDictionary } from "@/i18n/server";

const ORDER = ["learn", "help", "check", "report"] as const;

type FeatureKey = (typeof ORDER)[number];

const BANNERS: Record<
  FeatureKey,
  {
    tag: string;
    gradient: string;
    icon: React.ReactNode;
  }
> = {
  learn: {
    tag: "Security Education",
    gradient: "from-[#001433] via-[#00224f] to-[#003d99]",
    icon: (
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
        <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z" />
        <path d="M6 6h10" />
        <path d="M6 10h10" />
      </svg>
    ),
  },
  help: {
    tag: "Incident Recovery",
    gradient: "from-[#001f4d] via-[#002b66] to-[#0047b3]",
    icon: (
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
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        <path d="M12 8v4" />
        <path d="M12 16h.01" />
      </svg>
    ),
  },
  check: {
    tag: "Threat Scanner",
    gradient: "from-[#001433] via-[#002966] to-[#003d99]",
    icon: (
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
        <circle cx="11" cy="11" r="7" />
        <path d="m21 21-4.35-4.35" />
        <path d="m8 11 2 2 4-4" />
      </svg>
    ),
  },
  report: {
    tag: "Evidence & Directives",
    gradient: "from-[#001f4d] via-[#002b66] to-[#0047b3]",
    icon: (
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
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <path d="m9 15 2 2 4-4" />
      </svg>
    ),
  },
};

export default async function Features() {
  const { t } = await getDictionary();

  return (
    <section
      id="what"
      className="scroll-mt-24 relative bg-[#d8e1eb] dark:bg-[#001433] px-6 py-28 overflow-hidden transition-colors duration-300"
    >
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
          {ORDER.map((key) => {
            const banner = BANNERS[key];
            return (
              <li
                key={key}
                className="group relative flex flex-col justify-between rounded-[3px] border border-slate-300/80 bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-md dark:border-white/10 dark:bg-[#001433]/90 dark:shadow-none dark:hover:border-white/20"
              >
                <div>
                  {/* Top Graphic Banner matching the inspiration reference */}
                  <div
                    className={`relative flex h-36 w-full items-center justify-center overflow-hidden rounded-[3px] bg-gradient-to-br ${banner.gradient} text-white shadow-inner`}
                  >
                    <div
                      aria-hidden="true"
                      className="pointer-events-none absolute inset-0 bg-[radial-gradient(#ffffff18_1px,transparent_1px)] [background-size:12px_12px] opacity-70"
                    />
                    <div className="relative z-10 flex flex-col items-center gap-2 text-center px-3">
                      <div className="grid size-11 place-items-center rounded-[3px] border border-white/20 bg-white/10 text-white shadow-sm transition-transform duration-300 group-hover:scale-105">
                        {banner.icon}
                      </div>
                      <span className="text-[11px] font-bold tracking-wider uppercase text-blue-100">
                        {banner.tag}
                      </span>
                    </div>
                  </div>

                  <h3 className="mt-5 font-display text-lg font-bold text-slate-900 dark:text-white group-hover:text-[#004181] dark:group-hover:text-brand-lime transition-colors">
                    {t.what.cards[key].title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-300">
                    {t.what.cards[key].body}
                  </p>
                </div>

                {/* Card Action Button matching the inspiration reference */}
                <div className="mt-6 pt-2">
                  <a
                    href={key === "check" ? "#start" : "#how"}
                    className="inline-flex items-center justify-center rounded-[3px] bg-[#004181] hover:bg-[#002d5a] text-white px-5 py-2 text-xs font-bold uppercase tracking-wider shadow-sm transition-colors"
                  >
                    {t.what.seeMore}
                  </a>
                </div>
              </li>
            );
          })}
        </ul>

        {/* Centered Read More button below cards matching the inspiration reference */}
        <div className="mt-12 text-center">
          <a
            href="#how"
            className="inline-flex min-h-11 items-center justify-center rounded-[3px] border border-slate-300 bg-white hover:bg-slate-50 text-[#004181] px-8 text-sm font-bold shadow-sm transition-colors dark:border-white/20 dark:bg-white/5 dark:text-white dark:hover:bg-white/10"
          >
            {t.what.readMore}
          </a>
        </div>
      </div>
    </section>
  );
}
