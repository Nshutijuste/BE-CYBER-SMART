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
          className={`${rise} mb-5 inline-flex items-center gap-2 rounded-[2px] border border-brand-lime/30 bg-brand-lime/10 px-3.5 py-1 text-xs font-bold uppercase tracking-widest text-brand-lime shadow-[0_0_20px_rgba(77,184,20,0.2)] backdrop-blur-md`}
        >
          <span className="relative flex size-2">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-brand-lime opacity-75" />
            <span className="relative inline-flex size-2 rounded-full bg-brand-lime" />
          </span>
          Threat Prevention & Recovery
        </div>
        <h1
          className={`${rise} font-display text-2xl font-bold leading-[1.2] tracking-tight sm:text-3xl lg:text-4xl text-white [animation-delay:80ms]`}
        >
          {t.hero.title}
        </h1>
        <p
          className={`${rise} mt-4 max-w-lg text-sm sm:text-base leading-relaxed text-slate-300 [animation-delay:200ms]`}
        >
          {t.hero.body}
        </p>
        <div className={`${rise} mt-8 flex flex-wrap gap-4 [animation-delay:320ms]`}>
          <a
            href="#how"
            className={`inline-flex min-h-11 items-center rounded-[2px] bg-brand-lime px-6 py-2.5 text-sm sm:text-base font-bold text-brand-navy shadow-[0_0_20px_rgba(77,184,20,0.3)] transition-all duration-300 hover:bg-white hover:shadow-[0_0_30px_rgba(77,184,20,0.5)] ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-11 items-center rounded-[2px] border border-white/20 bg-white/5 px-6 py-2.5 text-sm sm:text-base font-bold text-white backdrop-blur-md transition-all duration-300 hover:border-brand-blue/50 hover:bg-white/10 hover:shadow-[0_0_20px_rgba(0,102,255,0.3)] ${focus}`}
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
