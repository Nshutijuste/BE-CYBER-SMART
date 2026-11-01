import Logo from "@/components/Logo";

export default function Header() {
  return (
    <header className="bg-slate-100">
      <div className="mx-auto flex max-w-6xl items-center px-6 py-4">
        <Logo />
      </div>
    </header>
  );
}