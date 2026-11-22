import { getDictionary } from "@/i18n/server";

export default async function HowItWorks() {
  const { t } = await getDictionary();

  return (
    <section id="how" className="relative bg-gradient-to-b from-[#f4f7fc] via-[#edf4ff] to-[#f4f7fc] dark:from-[#000714] dark:via-[#000d26] dark:to-[#000714] px-6 py-28 overflow-hidden transition-colors duration-300">
      {/* Background ambient lighting */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 size-[36rem] rounded-full bg-brand-blue/10 blur-3xl"
      />

      <div className="relative z-10 mx-auto max-w-6xl">
        <h2 className="font-display text-3xl font-extrabold text-slate-900 dark:text-white sm:text-4xl lg:text-[2.75rem] tracking-tight">
          {t.how.title}
        </h2>
        <ol className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {t.how.steps.map((step, i) => (
            <li
              key={step.title}
              className="group relative rounded-[3px] border border-slate-200/90 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1.5 hover:border-brand-blue/50 hover:shadow-md dark:border-white/10 dark:bg-white/[0.03] dark:shadow-none dark:backdrop-blur-md dark:hover:border-brand-blue/50 dark:hover:bg-white/[0.05] dark:hover:shadow-[0_10px_30px_-5px_rgba(0,102,255,0.25)]"
            >
              <span className="grid size-11 place-items-center rounded-[3px] bg-gradient-to-br from-brand-lime to-brand-green font-display text-lg font-black text-brand-navy shadow-[0_0_20px_rgba(77,184,20,0.45)] group-hover:scale-105 transition-transform duration-300">
                {i + 1}
              </span>
              <h3 className="mt-5 font-display text-xl font-bold text-slate-900 dark:text-white group-hover:text-brand-blue dark:group-hover:text-brand-lime transition-colors duration-300">
                {step.title}
              </h3>
              <p className="mt-2 text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
