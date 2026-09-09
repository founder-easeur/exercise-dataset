import Link from "next/link";
import { Card, LicenseBadge, PageHeader } from "@/components/ui";
import { serverGet } from "@/lib/server-api";

export const dynamic = "force-dynamic";

interface SourceRow {
  slug: string; name: string; domain: string; source_type: string; authority: string;
  license: string; commercial_use_allowed: string; attribution_required: boolean;
  robots_status: string; is_active: boolean; exercise_count?: number; document_count?: number;
  last_crawl?: { job_id: number; mode: string; status: string; finished_at: string | null } | null;
}

const AUTHORITY_STYLES: Record<string, string> = {
  high: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  medium: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
  unknown: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300",
};

export default async function SourcesPage() {
  const { items } = await serverGet<{ total: number; items: SourceRow[] }>("/api/v1/sources");
  const sorted = [...items].sort((a, b) => (b.exercise_count || 0) - (a.exercise_count || 0));

  return (
    <div>
      <PageHeader
        title="Sources"
        subtitle={`${items.length} registered sources. Only high-authority medical organizations and government health services are crawled; each carries a recorded license posture.`}
      />

      <div className="grid gap-3 md:grid-cols-2">
        {sorted.map((s) => (
          <Link key={s.slug} href={`/sources/${s.slug}`}
            className="card p-4 transition hover:border-brand-400 dark:hover:border-brand-700">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="font-medium">{s.name}</div>
                <div className="text-xs text-muted">{s.domain}</div>
              </div>
              <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${AUTHORITY_STYLES[s.authority] || AUTHORITY_STYLES.unknown}`}>
                {s.authority} authority
              </span>
            </div>
            <div className="mt-3 flex flex-wrap items-center gap-1.5 text-[11px]">
              <LicenseBadge license={s.license} />
              <span className="rounded-full bg-slate-100 px-2 py-0.5 capitalize dark:bg-slate-800">
                {s.source_type.replace(/_/g, " ")}
              </span>
              {s.attribution_required ? (
                <span className="rounded-full bg-slate-100 px-2 py-0.5 dark:bg-slate-800">attribution</span>
              ) : null}
              <span className="rounded-full bg-slate-100 px-2 py-0.5 dark:bg-slate-800">
                robots: {s.robots_status.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 flex items-center gap-4 text-xs text-muted">
              <span><strong className="text-slate-900 dark:text-slate-100">{s.exercise_count ?? 0}</strong> exercises</span>
              <span><strong className="text-slate-900 dark:text-slate-100">{s.document_count ?? 0}</strong> docs</span>
              {s.last_crawl ? (
                <span className="capitalize">last crawl: {s.last_crawl.status.replace(/_/g, " ")}</span>
              ) : (
                <span>not crawled yet</span>
              )}
              {!s.is_active ? <span className="text-rose-500">inactive</span> : null}
            </div>
          </Link>
        ))}
      </div>

      <Card className="mt-5 p-5 text-sm leading-relaxed text-muted">
        <strong className="text-slate-900 dark:text-slate-100">Crawler policy.</strong> The pipeline
        identifies itself (EaseurExerciseBot/1.0), respects robots.txt (snapshots stored per domain),
        rate-limits conservatively, never executes scraped JavaScript, validates every target URL
        against SSRF (private networks and cloud metadata are blocked), sanitizes all HTML, and stores
        only bounded excerpts rather than full articles. Sources whose terms don&apos;t clearly permit
        reuse are marked <em>unknown license</em> and excluded from redistribution until reviewed.
      </Card>
    </div>
  );
}
