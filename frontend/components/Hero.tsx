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
      className="relative z-10 mx-auto grid w-full max-w-6xl flex-1 items-center gap-12 px-6 pb-36 pt-28 md:grid-cols-[1.1fr_0.9fr] md:pb-44 md:pt-36"
    >
      <div>
        <div
          className={`${rise} mb-6 inline-flex items-center gap-2 rounded-full border border-brand-lime/30 bg-brand-lime/10 px-4 py-1.5 text-xs font-bold uppercase tracking-widest text-brand-lime shadow-[0_0_20px_rgba(77,184,20,0.25)] backdrop-blur-md`}
        >
          <span className="relative flex size-2">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-brand-lime opacity-75" />
            <span className="relative inline-flex size-2 rounded-full bg-brand-lime" />
          </span>
          AI-Powered Threat Prevention
        </div>
        <h1
          className={`${rise} font-display text-4xl font-extrabold leading-[1.15] tracking-tight sm:text-5xl lg:text-6xl text-white [animation-delay:80ms]`}
        >
          {t.hero.title}
        </h1>
        <p
          className={`${rise} mt-6 max-w-xl text-lg leading-relaxed text-slate-300 md:text-xl [animation-delay:200ms]`}
        >
          {t.hero.body}
        </p>
        <div className={`${rise} mt-9 flex flex-wrap gap-4 [animation-delay:320ms]`}>
          <a
            href="#how"
            className={`inline-flex min-h-14 items-center rounded-xl bg-brand-lime px-8 text-lg font-bold text-brand-navy shadow-[0_0_30px_rgba(77,184,20,0.35)] transition-all duration-300 hover:-translate-y-1 hover:bg-white hover:shadow-[0_0_40px_rgba(77,184,20,0.6)] ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-14 items-center rounded-xl border border-white/20 bg-white/5 px-8 text-lg font-bold text-white backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-brand-blue/50 hover:bg-white/10 hover:shadow-[0_0_25px_rgba(0,102,255,0.3)] ${focus}`}
          >
            {t.hero.scammed}
          </a>
        </div>
      </div>

      <div className={`${rise} [animation-delay:450ms]`}>
        <Orb safe={t.hero.chipSafe} risky={t.hero.chipRisk} />
      </div>
    </section>
  );
}
