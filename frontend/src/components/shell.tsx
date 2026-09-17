"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ThemeToggle } from "./theme";

const NAV = [
  { href: "/", label: "Dashboard", icon: "▦" },
  { href: "/exercises", label: "Exercises", icon: "☰" },
  { href: "/muscles", label: "Muscles", icon: " ⟐ " },
  { href: "/body-map", label: "Body Map", icon: "◍" },
  { href: "/coverage", label: "Coverage", icon: "▤" },
  { href: "/sources", label: "Sources", icon: "⌘" },
  { href: "/review", label: "Review Queue", icon: "✓" },
  { href: "/datasets", label: "Datasets", icon: "⬢" },
];

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const nav = (
    <nav className="space-y-0.5">
      {NAV.map((item) => {
        const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={() => setOpen(false)}
            className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition ${
              active
                ? "bg-brand-600 text-white shadow-sm"
                : "text-slate-600 hover:bg-brand-50 hover:text-brand-700 dark:text-slate-300 dark:hover:bg-brand-900/30 dark:hover:text-brand-300"
            }`}
          >
            <span className="w-5 text-center opacity-80">{item.icon}</span>
            {item.label}
          </Link>
        );
      })}
    </nav>
  );

  return (
    <div className="min-h-screen">
      {/* Top bar (mobile) */}
      <header className="sticky top-0 z-30 flex items-center justify-between border-b border-app bg-app/90 px-4 py-3 backdrop-blur md:hidden">
        <button className="rounded-md border border-app px-2.5 py-1.5 text-sm" onClick={() => setOpen(!open)}>
          ☰
        </button>
        <Link href="/" className="font-semibold tracking-tight">
          Easeur <span className="text-brand-600 dark:text-brand-400">Exercise KB</span>
        </Link>
        <ThemeToggle />
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`fixed inset-y-0 left-0 z-40 w-64 shrink-0 border-r border-app bg-card p-4 transition-transform md:sticky md:top-0 md:h-screen md:translate-x-0 ${
            open ? "translate-x-0" : "-translate-x-full"
          }`}
        >
          <div className="mb-6 flex items-center justify-between px-1">
            <Link href="/" className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-sm font-bold text-white">
                E
              </span>
              <span className="leading-tight">
                <span className="block text-sm font-semibold">Easeur</span>
                <span className="block text-xs text-muted">Exercise Knowledge Base</span>
              </span>
            </Link>
            <div className="hidden md:block">
              <ThemeToggle />
            </div>
          </div>
          {nav}
          <div className="absolute bottom-4 left-4 right-4 rounded-lg border border-app p-3 text-[11px] leading-relaxed text-muted">
            Research platform for{" "}
            <a href="https://workout.easeur.com" className="text-brand-600 hover:underline dark:text-brand-400">
              workout.easeur.com
            </a>
            . Structured facts + provenance only.
          </div>
        </aside>
        {open ? <div className="fixed inset-0 z-30 bg-black/30 md:hidden" onClick={() => setOpen(false)} /> : null}

        <main className="min-w-0 flex-1 px-4 py-6 md:px-8 md:py-8">{children}</main>
      </div>
    </div>
  );
}
