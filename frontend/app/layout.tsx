import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import "./globals.css";
import { getDictionary } from "@/i18n/server";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const montserrat = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin"],
  weight: ["600", "700", "800"],
});

export async function generateMetadata(): Promise<Metadata> {
  const { t } = await getDictionary();
  return {
    title: "Be Cyber Smart",
    description: t.meta.description,
  };
}

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const { locale } = await getDictionary();

  return (
    <html lang={locale} className={`${inter.variable} ${montserrat.variable} dark`} data-theme="dark" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('theme')||'dark';if(t==='dark'){document.documentElement.classList.add('dark');document.documentElement.classList.remove('light');document.documentElement.dataset.theme='dark'}else{document.documentElement.classList.remove('dark');document.documentElement.classList.add('light');document.documentElement.dataset.theme='light'}}catch(e){}})()`,
          }}
        />
      </head>
      <body className="min-h-screen bg-[#f4f7fc] font-sans text-slate-900 antialiased selection:bg-brand-lime selection:text-brand-navy transition-colors duration-300 dark:bg-[#001433] dark:text-slate-100">
        {children}
      </body>
    </html>
  );
}