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
    <section id="what" className="bg-white px-6 py-20">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-3xl font-extrabold text-brand-navy md:text-4xl">
          {t.what.title}
        </h2>
        <ul className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {ORDER.map((key, i) => (
            <li
              key={key}
              className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <span
                className={`grid size-12 place-items-center rounded-xl ${
                  i % 2 === 0
                    ? "bg-brand-blue/10 text-brand-blue"
                    : "bg-brand-green/10 text-brand-green"
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
              </span>
              <h3 className="mt-5 font-display text-xl font-bold text-brand-navy">
                {t.what.cards[key].title}
              </h3>
              <p className="mt-2 text-lg leading-relaxed text-slate-700">
                {t.what.cards[key].body}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}