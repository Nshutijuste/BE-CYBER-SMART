import Orb from "@/components/Orb";
import { getDictionary } from "@/i18n/server";

const focus =
  "focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime";

export default async function Hero() {
  const { t } = await getDictionary();

  return (
    <section
      id="start"
      className="mx-auto grid w-full max-w-6xl flex-1 items-center gap-12 px-6 pb-36 pt-28 md:grid-cols-[1.1fr_0.9fr] md:pb-44 md:pt-32"
    >
      <div>
        <h1 className="font-display text-4xl font-extrabold leading-tight sm:text-5xl">
          {t.hero.title}
        </h1>
        <p className="mt-6 max-w-xl text-lg leading-relaxed text-white/90 md:text-xl">
          {t.hero.body}
        </p>
        <div className="mt-9 flex flex-wrap gap-4">
          {/* These two will point to the real pages when we build them */}
          <a
            href="#how"
            className={`inline-flex min-h-14 items-center rounded-xl bg-brand-lime px-7 text-lg font-bold text-brand-navy hover:bg-white ${focus}`}
          >
            {t.hero.check}
          </a>
          <a
            href="#what"
            className={`inline-flex min-h-14 items-center rounded-xl border-2 border-white px-7 text-lg font-bold text-white hover:bg-white hover:text-brand-navy ${focus}`}
          >
            {t.hero.scammed}
          </a>
        </div>
      </div>

      <Orb safe={t.hero.chipSafe} risky={t.hero.chipRisk} />
    </section>
  );
}