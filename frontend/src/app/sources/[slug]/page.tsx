import Link from "next/link";
import { notFound } from "next/navigation";
import { Badge, Card, LicenseBadge, PageHeader, StatCard } from "@/components/ui";
import { serverGet } from "@/lib/server-api";

export const dynamic = "force-dynamic";

interface SourceRow {
  slug: string; name: string; domain: string; homepage_url?: string | null;
  source_type: string; authority: string; license: string;
  commercial_use_allowed: string; attribution_required: boolean;
  robots_status: string; is_active: boolean; notes?: string | null;
  exercise_count?: number; document_count?: number;
  last_crawl?: { job_id: number; mode: string; status: string; finished_at: string | null } | null;
  documents?: { id: number; url: string; title: string | null; fetched_at: string | null; word_count: number | null }[];
}

const TYPE_LABELS: Record<string, string> = {
  medical_org: "Medical organization",
  government: "Government health service",
  nonprofit: "Non-profit",
  clinical: "Clinical reference",
  academic: "Academic",
};

export default async function SourceDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  let src: SourceRow;
  try {
    src = await serverGet<SourceRow>(`/api/v1/sources/${slug}`);
  } catch {
    notFound();
  }

  return (
    <div>
      <div className="mb-2 text-sm text-muted">
        <Link href="/sources" className="hover:text-brand-600 dark:hover:text-brand-400">← All sources</Link>
      </div>
      <PageHeader
        title={src.name}
        subtitle={src.domain}
        actions={
          src.homepage_url ? (
            <a href={src.homepage_url} target="_blank" rel="noreferrer"
              className="rounded-lg border border-app px-3 py-1.5 text-sm hover:border-brand-400">
              Visit site ↗
            </a>
          ) : null
        }
      />

      <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-4">
        <StatCard label="Exercises sourced" value={src.exercise_count ?? 0} tone="brand" />
        <StatCard label="Documents crawled" value={src.document_count ?? 0} />
        <StatCard label="Authority" value={src.authority} tone={src.authority === "high" ? "good" : "default"} />
        <StatCard label="Robots.txt" value={src.robots_status.replace(/_/g, " ")} />
      </div>

      <div className="grid gap-5 lg:grid-cols-3">
        <Card className="p-5 lg:col-span-1">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">Licensing</h2>
          <div className="space-y-2.5 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-muted">License</span> <LicenseBadge license={src.license} />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Commercial use</span>
              <Badge className={
                src.commercial_use_allowed === "yes"
                  ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300"
                  : src.commercial_use_allowed === "no"
                    ? "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300"
                    : "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300"
              }>{src.commercial_use_allowed.replace(/_/g, " ")}</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Attribution</span>
              <span>{src.attribution_required ? "Required" : "Not required"}</span>
            </div>
            {src.notes ? <p className="pt-2 text-xs leading-relaxed text-muted">{src.notes}</p> : null}
            <p className="pt-2 text-xs leading-relaxed text-muted">
              The crawler stores structured facts, metadata and bounded excerpts with links back to the
              original page — never full copyrighted article text or media.
            </p>
          </div>
        </Card>

        <Card className="p-5 lg:col-span-2">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">Crawled documents</h2>
          {src.documents && src.documents.length > 0 ? (
            <div className="space-y-2">
              {src.documents.map((d) => (
                <a key={d.id} href={d.url} target="_blank" rel="noreferrer"
                  className="block rounded-lg border border-app p-3 transition hover:border-brand-400">
                  <div className="text-sm font-medium">{d.title || d.url}</div>
                  <div className="mt-0.5 flex flex-wrap gap-2 text-[11px] text-muted">
                    <span className="truncate">{d.url}</span>
                    {d.word_count ? <span>· ~{d.word_count} words</span> : null}
                    {d.fetched_at ? <span>· fetched {new Date(d.fetched_at).toLocaleDateString()}</span> : null}
                  </div>
                </a>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted">
              No documents crawled from this source yet. It is registered for future aggregation runs.
            </p>
          )}
        </Card>
      </div>
    </div>
  );
}
