import type { Metadata } from "next";
import { Geist, Montserrat } from "next/font/google";
import "./globals.css";
import { getDictionary } from "@/i18n/server";

const geist = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const montserrat = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin"],
  weight: ["600", "700", "800"],
});

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getDictionary();
  return { title: "Be Cyber Smart", description: t.meta.description };
}

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const { locale } = await getDictionary();
  return (
    <html lang={locale} className={`${geist.variable} ${montserrat.variable}`}>
      <body className="min-h-screen bg-white font-sans text-slate-800 antialiased">
        {children}
      </body>
    </html>
  );
}