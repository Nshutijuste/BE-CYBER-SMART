import { getDictionary } from "@/i18n/server";

export default async function GoldenRule() {
  const { t } = await getDictionary();

  return (
    <section
      id="rule"
      className="bg-linear-to-br from-brand-navy via-calm to-brand-blue px-6 py-20 text-white"
    >
      <div className="mx-auto max-w-4xl border-l-8 border-brand-lime pl-6 md:pl-10">
        <h2 className="font-display text-3xl font-extrabold leading-snug md:text-4xl">
          {t.rule.title}
        </h2>
        <p className="mt-5 text-lg leading-relaxed text-white/90 md:text-xl">
          {t.rule.body}
        </p>
      </div>
    </section>
  );
}