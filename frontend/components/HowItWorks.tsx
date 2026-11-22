import { getDictionary } from "@/i18n/server";

export default async function HowItWorks() {
  const { t } = await getDictionary();

  return (
    <section id="how" className="scroll-mt-24 relative bg-[#d8e1eb] dark:bg-gradient-to-b dark:from-[#001433] dark:via-[#001f4d] dark:to-[#001433] px-6 py-28 overflow-hidden transition-colors duration-300">
      {/* Background ambient lighting (dark theme only) */}
      <div
        aria-hidden="true"
        className="hidden dark:block pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 size-[36rem] rounded-full bg-brand-blue/10 blur-3xl"
      />

      <div className="relative z-10 mx-auto max-w-6xl">
        <h2 className="font-display text-3xl font-extrabold text-slate-900 dark:text-white sm:text-4xl lg:text-[2.75rem] tracking-tight">
          {t.how.title}
        </h2>
        <ol className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {t.how.steps.map((step, i) => (
            <li
              key={step.title}
              className="group relative rounded-[3px] border border-slate-200/90 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1.5 hover:border-brand-blue/50 hover:shadow-md dark:border-blue-400/25 dark:bg-[#0b2b5c]/85 dark:shadow-[0_12px_32px_-8px_rgba(0,0,0,0.6),inset_0_1px_0_0_rgba(255,255,255,0.18)] dark:hover:border-blue-300/40 dark:hover:bg-[#0e3570]"
            >
              <span className="grid size-11 place-items-center rounded-[3px] bg-[#004181] text-white shadow-md shadow-[#004181]/25 dark:bg-gradient-to-br dark:from-brand-lime dark:to-brand-green dark:text-brand-navy dark:shadow-[0_0_20px_rgba(77,184,20,0.45)] font-display text-[19px] font-black group-hover:scale-105 transition-transform duration-300">
                {i + 1}
              </span>
              <h3 className="mt-5 font-display text-xl font-bold text-slate-900 dark:text-white group-hover:text-[#004181] dark:group-hover:text-brand-lime transition-colors duration-300">
                {step.title}
              </h3>
              <p className="mt-2 text-[15px] sm:text-[17px] leading-relaxed text-slate-600 dark:text-slate-300">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
