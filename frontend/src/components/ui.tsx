import Link from "next/link";
import type { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`card ${className}`}>{children}</div>;
}

export function StatCard({
  label,
  value,
  href,
  tone = "default",
  hint,
}: {
  label: string;
  value: number | string;
  href?: string;
  tone?: "default" | "good" | "warn" | "bad" | "brand";
  hint?: string;
}) {
  const tones: Record<string, string> = {
    default: "text-slate-900 dark:text-slate-100",
    good: "text-emerald-600 dark:text-emerald-400",
    warn: "text-amber-600 dark:text-amber-400",
    bad: "text-rose-600 dark:text-rose-400",
    brand: "text-brand-600 dark:text-brand-400",
  };
  const inner = (
    <div className="card p-4 transition hover:border-brand-300 dark:hover:border-brand-700">
      <div className="text-xs font-medium uppercase tracking-wide text-muted">{label}</div>
      <div className={`mt-1 text-2xl font-semibold ${tones[tone]}`}>{value}</div>
      {hint ? <div className="mt-0.5 text-xs text-muted">{hint}</div> : null}
    </div>
  );
  return href ? <Link href={href}>{inner}</Link> : inner;
}

const REVIEW_STATUS_STYLES: Record<string, string> = {
  approved: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  pending_review: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  rejected: "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300",
  flagged: "bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300",
  draft: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300",
};

const GENERIC_BADGE: Record<string, string> = {
  curated: "bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300",
  aggregated: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
  medical: "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300",
};

export function Badge({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium ${className}`}>
      {children}
    </span>
  );
}

export function ReviewStatusPill({ status }: { status: string }) {
  return <Badge className={REVIEW_STATUS_STYLES[status] || REVIEW_STATUS_STYLES.draft}>{status.replace("_", " ")}</Badge>;
}

export function OriginBadge({ origin }: { origin: string }) {
  if (GENERIC_BADGE[origin])
    return <Badge className={GENERIC_BADGE[origin]}>{origin}</Badge>;
  return <Badge className={REVIEW_STATUS_STYLES.draft}>{origin}</Badge>;
}

export function MedicalBadge() {
  return <Badge className={GENERIC_BADGE.medical}>⚠ medical claim</Badge>;
}

export function LicenseBadge({ license }: { license: string }) {
  const styles: Record<string, string> = {
    public_domain: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
    cc0: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
    cc_by: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
    open_data: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
    unknown: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
    restricted: "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300",
  };
  return <Badge className={styles[license] || styles.unknown}>{license.replace(/_/g, " ")}</Badge>;
}

export function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const tone = pct >= 85 ? "bg-emerald-500" : pct >= 65 ? "bg-amber-500" : "bg-rose-500";
  return (
    <div className="flex items-center gap-2" title={`Confidence ${pct}%`}>
      <div className="h-1.5 w-16 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
        <div className={`h-full rounded-full ${tone}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-[11px] text-muted">{pct}%</span>
    </div>
  );
}

export function CoverageStatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    excellent: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
    good: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
    limited: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
    missing: "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300",
    needs_review: "bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300",
  };
  const labels: Record<string, string> = { needs_review: "needs review" };
  return <Badge className={styles[status] || styles.missing}>{labels[status] || status}</Badge>;
}

export function PageHeader({ title, subtitle, actions }: { title: string; subtitle?: string; actions?: ReactNode }) {
  return (
    <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        {subtitle ? <p className="mt-1 text-sm text-muted">{subtitle}</p> : null}
      </div>
      {actions}
    </div>
  );
}

export function EmptyState({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="card flex flex-col items-center justify-center gap-2 p-12 text-center">
      <div className="text-base font-medium">{title}</div>
      {hint ? <div className="text-sm text-muted">{hint}</div> : null}
    </div>
  );
}

export function BarList({
  items,
  max,
  hrefBase,
  unit = "",
}: {
  items: { slug: string; name: string; count: number }[];
  max?: number;
  hrefBase?: string;
  unit?: string;
}) {
  const peak = max ?? Math.max(1, ...items.map((i) => i.count));
  return (
    <div className="space-y-2.5">
      {items.map((item) => {
        const bar = (
          <div className="group flex items-center gap-3">
            <div className="w-36 shrink-0 truncate text-sm" title={item.name}>
              {hrefBase ? (
                <Link href={`${hrefBase}${item.slug}`} className="hover:text-brand-600 dark:hover:text-brand-400">
                  {item.name}
                </Link>
              ) : (
                item.name
              )}
            </div>
            <div className="h-5 flex-1 overflow-hidden rounded bg-slate-100 dark:bg-slate-800">
              <div
                className="flex h-full items-center justify-end rounded bg-brand-500/80 pr-1.5 text-[10px] font-medium text-white transition group-hover:bg-brand-500"
                style={{ width: `${Math.max(6, (item.count / peak) * 100)}%` }}
              >
                {item.count}
                {unit}
              </div>
            </div>
          </div>
        );
        return <div key={item.slug}>{bar}</div>;
      })}
    </div>
  );
}

export function Donut({ segments, size = 140, label }: { segments: { value: number; color: string; name: string }[]; size?: number; label?: string }) {
  const total = segments.reduce((s, x) => s + x.value, 0) || 1;
  const radius = size / 2 - 14;
  const circumference = 2 * Math.PI * radius;
  let offset = 0;
  return (
    <div className="flex items-center gap-5">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <g transform={`rotate(-90 ${size / 2} ${size / 2})`}>
          {segments.map((seg, i) => {
            const len = (seg.value / total) * circumference;
            const el = (
              <circle
                key={i}
                cx={size / 2}
                cy={size / 2}
                r={radius}
                fill="none"
                stroke={seg.color}
                strokeWidth={16}
                strokeDasharray={`${len} ${circumference - len}`}
                strokeDashoffset={-offset}
                strokeLinecap="butt"
              />
            );
            offset += len;
            return el;
          })}
        </g>
        {label ? (
          <text x="50%" y="47%" textAnchor="middle" className="fill-slate-900 dark:fill-slate-100" fontSize="20" fontWeight="600">
            {total}
          </text>
        ) : null}
        {label ? (
          <text x="50%" y="60%" textAnchor="middle" className="fill-slate-500" fontSize="10">
            {label}
          </text>
        ) : null}
      </svg>
      <div className="space-y-1.5">
        {segments.map((seg, i) => (
          <div key={i} className="flex items-center gap-2 text-sm">
            <span className="h-2.5 w-2.5 rounded-sm" style={{ background: seg.color }} />
            <span className="text-muted">{seg.name}</span>
            <span className="font-medium">{seg.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function Pagination({
  page,
  pageSize,
  total,
  onPage,
}: {
  page: number;
  pageSize: number;
  total: number;
  onPage: (p: number) => void;
}) {
  const pages = Math.ceil(total / pageSize) || 1;
  if (pages <= 1) return null;
  const window: (number | "…")[] = [];
  for (let i = 1; i <= pages; i++) {
    if (i === 1 || i === pages || Math.abs(i - page) <= 1) window.push(i);
    else if (window[window.length - 1] !== "…") window.push("…");
  }
  return (
    <div className="flex items-center justify-between gap-3 border-t border-app pt-4">
      <div className="text-xs text-muted">
        {(page - 1) * pageSize + 1}–{Math.min(page * pageSize, total)} of {total}
      </div>
      <div className="flex items-center gap-1">
        <button
          className="rounded-md border border-app px-2.5 py-1 text-sm disabled:opacity-40"
          disabled={page <= 1}
          onClick={() => onPage(page - 1)}
        >
          ‹
        </button>
        {window.map((p, i) =>
          p === "…" ? (
            <span key={`e${i}`} className="px-1 text-muted">
              …
            </span>
          ) : (
            <button
              key={p}
              className={`rounded-md px-3 py-1 text-sm ${p === page ? "bg-brand-600 text-white" : "border border-app hover:bg-brand-50 dark:hover:bg-brand-900/30"}`}
              onClick={() => onPage(p)}
            >
              {p}
            </button>
          ),
        )}
        <button
          className="rounded-md border border-app px-2.5 py-1 text-sm disabled:opacity-40"
          disabled={page >= pages}
          onClick={() => onPage(page + 1)}
        >
          ›
        </button>
      </div>
    </div>
  );
}

export function KeyValue({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex gap-3 py-1.5 text-sm">
      <div className="w-40 shrink-0 text-muted">{label}</div>
      <div className="flex-1">{children}</div>
    </div>
  );
}
