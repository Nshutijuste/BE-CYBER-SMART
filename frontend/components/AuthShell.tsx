import Header from "@/components/Header";

export default function AuthShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="relative flex min-h-dvh flex-col overflow-hidden bg-gradient-to-b from-[#000e26] via-[#000819] to-[#000714] text-white">
      {/* Subtle cybernetic dot grid overlay */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(#ffffff0a_1px,transparent_1px)] [background-size:28px_28px] opacity-75"
      />
      {/* Ambient cosmic glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -left-32 top-1/4 size-[28rem] rounded-full bg-brand-blue/20 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 bottom-10 size-[28rem] rounded-full bg-brand-lime/10 blur-3xl"
      />

      <Header />
      <main className="relative z-10 flex flex-1 items-center justify-center px-4 pb-16 pt-28">
        <div className="w-full max-w-md rounded-3xl bg-white p-7 shadow-2xl sm:p-9 ring-1 ring-black/5">
          <h1 className="font-display text-3xl font-extrabold text-brand-navy">{title}</h1>
          {children}
        </div>
      </main>
    </div>
  );
}
