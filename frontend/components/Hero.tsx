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
        <h1
          className={`${rise} font-display text-3xl font-bold leading-[1.2] tracking-tight sm:text-4xl lg:text-[2.75rem] text-slate-900 dark:text-white [animation-delay:80ms]`}
        >
          {t.hero.title}
        </h1>
        <p
          className={`${rise} mt-5 max-w-lg text-[17px] sm:text-[19px] leading-relaxed text-slate-600 dark:text-slate-300 [animation-delay:200ms]`}
        >
          {t.hero.body}
        </p>
        <div className={`${rise} mt-9 flex flex-wrap gap-4 [animation-delay:320ms]`}>
          <a
            href="#how"
            className={`inline-flex min-h-12 items-center rounded-[3px] bg-[#004181] hover:bg-[#003466] text-white shadow-md dark:bg-brand-lime dark:text-brand-navy dark:shadow-[0_0_20px_rgba(77,184,20,0.3)] dark:hover:bg-white px-7 py-3 text-[17px] sm:text-[18px] font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-12 items-center rounded-[3px] border border-slate-300 bg-white/80 text-slate-800 hover:bg-white hover:border-[#004181]/50 dark:border-white/20 dark:bg-white/5 dark:text-white dark:backdrop-blur-md dark:hover:border-brand-blue/50 dark:hover:bg-white/10 px-7 py-3 text-[17px] sm:text-[18px] font-bold transition-all duration-300 ${focus}`}
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
