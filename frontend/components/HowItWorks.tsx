import { getDictionary } from "@/i18n/server";

export default async function HowItWorks() {
  const { t } = await getDictionary();

  return (
    <section id="how" className="relative bg-gradient-to-b from-[#000714] via-[#000d26] to-[#000714] px-6 py-28 overflow-hidden">
      {/* Background ambient lighting */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 size-[36rem] rounded-full bg-brand-blue/10 blur-3xl"
      />

      <div className="relative z-10 mx-auto max-w-6xl">
        <div className="inline-flex items-center gap-2 rounded-full border border-brand-blue/30 bg-brand-blue/10 px-3.5 py-1 text-xs font-bold uppercase tracking-wider text-brand-blue mb-3">
          Step-by-Step Flow
        </div>
        <h2 className="font-display text-3xl font-extrabold text-white md:text-5xl tracking-tight">
          {t.how.title}
        </h2>
        <ol className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {t.how.steps.map((step, i) => (
            <li
              key={step.title}
              className="group relative rounded-2xl border border-white/10 bg-white/[0.03] p-7 backdrop-blur-md transition-all duration-300 hover:-translate-y-1.5 hover:border-brand-blue/50 hover:bg-white/[0.05] hover:shadow-[0_10px_30px_-5px_rgba(0,102,255,0.25)]"
            >
              <span className="grid size-12 place-items-center rounded-xl bg-gradient-to-br from-brand-lime to-brand-green font-display text-lg font-black text-brand-navy shadow-[0_0_25px_rgba(77,184,20,0.45)] group-hover:scale-110 transition-transform duration-300">
                {i + 1}
              </span>
              <h3 className="mt-5 font-display text-xl font-bold text-white group-hover:text-brand-lime transition-colors duration-300">
                {step.title}
              </h3>
              <p className="mt-2 text-base leading-relaxed text-slate-300">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
