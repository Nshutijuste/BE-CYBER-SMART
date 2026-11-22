import Orb from "@/components/Orb";
import { getDictionary } from "@/i18n/server";

const focus =
  "focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime";
const rise = "motion-safe:animate-rise";

export default async function Hero() {
  const { t } = await getDictionary();

  return (
    <section
      id="start"
      className="relative z-10 mx-auto grid w-full max-w-7xl flex-1 items-center gap-16 px-6 pb-28 pt-28 sm:px-8 lg:grid-cols-2 lg:gap-24 xl:gap-32 md:pb-36 md:pt-32"
    >
      <div className="max-w-xl">
        <div
          className={`${rise} mb-5 inline-flex items-center gap-2 rounded-[2px] border border-brand-blue/30 bg-brand-blue/10 text-brand-blue dark:border-brand-lime/30 dark:bg-brand-lime/10 dark:text-brand-lime px-3.5 py-1 text-xs font-bold uppercase tracking-widest shadow-sm dark:shadow-[0_0_20px_rgba(77,184,20,0.2)] backdrop-blur-md`}
        >
          <span className="relative flex size-2">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-brand-blue dark:bg-brand-lime opacity-75" />
            <span className="relative inline-flex size-2 rounded-full bg-brand-blue dark:bg-brand-lime" />
          </span>
          Threat Prevention & Recovery
        </div>
        <h1
          className={`${rise} font-display text-2xl font-bold leading-[1.2] tracking-tight sm:text-3xl lg:text-4xl text-slate-900 dark:text-white [animation-delay:80ms]`}
        >
          {t.hero.title}
        </h1>
        <p
          className={`${rise} mt-4 max-w-lg text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300 [animation-delay:200ms]`}
        >
          {t.hero.body}
        </p>
        <div className={`${rise} mt-8 flex flex-wrap gap-4 [animation-delay:320ms]`}>
          <a
            href="#how"
            className={`inline-flex min-h-11 items-center rounded-[2px] bg-brand-blue text-white shadow-md hover:bg-brand-navy dark:bg-brand-lime dark:text-brand-navy dark:shadow-[0_0_20px_rgba(77,184,20,0.3)] dark:hover:bg-white px-6 py-2.5 text-sm sm:text-base font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-11 items-center rounded-[2px] border border-slate-300 bg-white/80 text-slate-800 hover:bg-white hover:border-brand-blue/50 dark:border-white/20 dark:bg-white/5 dark:text-white dark:backdrop-blur-md dark:hover:border-brand-blue/50 dark:hover:bg-white/10 px-6 py-2.5 text-sm sm:text-base font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.scammed}
          </a>
        </div>
      </div>

      <div className={`${rise} flex justify-center lg:justify-end [animation-delay:450ms]`}>
        <Orb safe={t.hero.chipSafe} risky={t.hero.chipRisk} />
      </div>
    </section>
  );
}
