import { cookies } from "next/headers";
import { defaultLocale, isLocale, localeCookie, type Locale } from "@/i18n/config";

const dictionaries = {
  en: () => import("@/i18n/dictionaries/en.json").then((m) => m.default),
  rw: () => import("@/i18n/dictionaries/rw.json").then((m) => m.default),
  fr: () => import("@/i18n/dictionaries/fr.json").then((m) => m.default),
};

export async function getLocale(): Promise<Locale> {
  const value = (await cookies()).get(localeCookie)?.value;
  return isLocale(value) ? value : defaultLocale;
}

export async function getDictionary() {
  const locale = await getLocale();
  return { locale, t: await dictionaries[locale]() };
}