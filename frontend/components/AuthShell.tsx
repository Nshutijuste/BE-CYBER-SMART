import Header from "@/components/Header";

export default function AuthShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="relative flex min-h-dvh flex-col bg-linear-to-br from-calm to-brand-navy">
      <Header />
      <main className="flex flex-1 items-center justify-center px-4 pb-16 pt-28">
        <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl sm:p-8">
          <h1 className="font-display text-3xl font-extrabold text-brand-navy">{title}</h1>
          {children}
        </div>
      </main>
    </div>
  );
}
