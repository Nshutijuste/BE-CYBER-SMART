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
      className="relative z-10 mx-auto grid w-full max-w-7xl flex-1 items-center gap-10 px-4 pb-20 pt-28 sm:px-8 md:grid-cols-2 md:gap-16 lg:gap-24 xl:gap-32 md:pb-36 md:pt-36"
    >
      <div className="max-w-xl text-center md:text-left mx-auto md:mx-0">
        <h1
          className={`${rise} font-display text-3xl font-extrabold leading-[1.2] tracking-tight sm:text-4xl lg:text-[2.75rem] text-slate-900 dark:text-white [animation-delay:80ms]`}
        >
          {t.hero.title}
        </h1>
        <p
          className={`${rise} mt-5 max-w-lg text-[17px] sm:text-[19px] leading-relaxed text-slate-600 dark:text-slate-300 [animation-delay:200ms]`}
        >
          {t.hero.body}
        </p>
        <div className={`${rise} mt-8 sm:mt-9 flex flex-col sm:flex-row flex-wrap justify-center md:justify-start gap-3 sm:gap-4 [animation-delay:320ms]`}>
          <a
            href="#how"
            className={`inline-flex min-h-12 w-full sm:w-auto items-center justify-center rounded-[3px] bg-[#005bb5] hover:bg-[#004d99] text-white shadow-md dark:bg-[#0066ff] dark:hover:bg-[#1a75ff] dark:text-white dark:shadow-[0_4px_24px_rgba(0,102,255,0.4)] px-7 py-3 text-[17px] sm:text-[18px] font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-12 w-full sm:w-auto items-center justify-center rounded-[3px] border border-slate-300 bg-white/90 hover:bg-white hover:border-[#005bb5]/50 text-slate-800 shadow-sm dark:border-white/30 dark:bg-white/10 dark:text-white dark:backdrop-blur-md dark:hover:bg-white/20 dark:hover:border-white/50 px-7 py-3 text-[17px] sm:text-[18px] font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.scammed}
          </a>
        </div>
      </div>

      <div className={`${rise} hidden md:flex justify-center md:justify-end [animation-delay:450ms]`}>
        <Orb safe={t.hero.chipSafe} risky={t.hero.chipRisk} />
      </div>
    </section>
  );
}
