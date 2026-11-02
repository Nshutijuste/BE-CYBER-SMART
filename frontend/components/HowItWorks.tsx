import { getDictionary } from "@/i18n/server";

export default async function HowItWorks() {
  const { t } = await getDictionary();

  return (
    <section id="how" className="bg-sky/25 px-6 py-20">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-3xl font-extrabold text-brand-navy md:text-4xl">
          {t.how.title}
        </h2>
        <ol className="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {t.how.steps.map((step, i) => (
            <li key={step.title}>
              <span className="grid size-12 place-items-center rounded-full bg-brand-blue font-display text-xl font-extrabold text-white">
                {i + 1}
              </span>
              <h3 className="mt-5 font-display text-xl font-bold text-brand-navy">
                {step.title}
              </h3>
              <p className="mt-2 text-lg leading-relaxed text-slate-700">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}