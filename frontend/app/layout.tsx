import type { Metadata } from "next";
import { Geist, Montserrat } from "next/font/google";
import "./globals.css";

const geist = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const montserrat = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin"],
  weight: ["600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Be Cyber Smart",
  description: "Learn to spot scams, check messages, and get help fast. English and Kinyarwanda.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${geist.variable} ${montserrat.variable}`}>
      <body className="min-h-screen bg-white font-sans text-slate-800 antialiased">
        {children}
      </body>
    </html>
  );
}