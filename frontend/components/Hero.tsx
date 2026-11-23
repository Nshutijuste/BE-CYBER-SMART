import { getDictionary } from "@/i18n/server";

const focus =
  "focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime";
const rise = "motion-safe:animate-rise";

export default async function Hero() {
  const { t } = await getDictionary();

  return (
    <section
      id="start"
      className="relative z-10 mx-auto flex w-full max-w-4xl flex-1 flex-col items-center justify-center text-center px-4 pb-24 pt-32 sm:px-8 sm:pt-36 md:pb-36 md:pt-40"
    >
      <div className="max-w-2xl">
        <h1
          className={`${rise} font-display text-3xl font-extrabold leading-[1.2] tracking-tight sm:text-5xl lg:text-[3.25rem] text-slate-900 dark:text-white [animation-delay:80ms]`}
        >
          {t.hero.title}
        </h1>
        <p
          className={`${rise} mt-6 max-w-xl mx-auto text-[18px] sm:text-[20px] leading-relaxed text-slate-600 dark:text-slate-300 [animation-delay:200ms]`}
        >
          {t.hero.body}
        </p>
        <div className={`${rise} mt-9 flex flex-col sm:flex-row flex-wrap items-center justify-center gap-4 [animation-delay:320ms]`}>
          <a
            href="#how"
            className={`inline-flex min-h-12 w-full sm:w-auto items-center justify-center rounded-[3px] bg-[#004181] hover:bg-[#003466] text-white shadow-md dark:bg-[#004181] dark:hover:bg-[#003466] dark:text-white dark:shadow-[0_4px_20px_rgba(0,65,129,0.35)] px-8 py-3.5 text-[17px] sm:text-[18px] font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-12 w-full sm:w-auto items-center justify-center rounded-[3px] border border-slate-300 bg-white/80 text-slate-800 hover:bg-white hover:border-[#004181]/50 dark:border-white/20 dark:bg-white/10 dark:text-white dark:backdrop-blur-md dark:hover:border-white/40 dark:hover:bg-white/15 px-8 py-3.5 text-[17px] sm:text-[18px] font-bold transition-all duration-300 ${focus}`}
          >
            {t.hero.scammed}
          </a>
        </div>
      </div>
    </section>
  );
}
