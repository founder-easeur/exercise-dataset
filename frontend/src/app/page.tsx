import Link from "next/link";
import { BarList, Card, Donut, PageHeader, StatCard } from "@/components/ui";
import { serverGet } from "@/lib/server-api";
import type { DashboardStats } from "@/lib/api";

export const dynamic = "force-dynamic";

const CATEGORY_COLORS = [
  "#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#ec4899", "#f43f5e",
  "#f97316", "#f59e0b", "#eab308", "#84cc16", "#22c55e", "#14b8a6",
];

export default async function DashboardPage() {
  const stats = await serverGet<DashboardStats>("/api/v1/stats/dashboard");

  const coveragePct = Math.round((stats.muscles_covered / Math.max(1, stats.muscles_total)) * 100);

  return (
    <div>
      <PageHeader
        title="Exercise Knowledge Base"
        subtitle="Stretching · mobility · physiotherapy-oriented · rehabilitation — with provenance, licensing and review workflows."
        actions={
          <div className="flex gap-2">
            <Link
              href="/exercises"
              className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-brand-700"
            >
              Browse exercises
            </Link>
            <Link
              href="/review"
              className="rounded-lg border border-app px-4 py-2 text-sm font-medium transition hover:border-brand-400"
            >
              Review queue ({stats.open_review_items})
            </Link>
          </div>
        }
      />

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-5">
        <StatCard label="Total exercises" value={stats.total_exercises} href="/exercises" tone="brand"
          hint={`${stats.curated_exercises} curated · ${stats.aggregated_exercises} aggregated`} />
        <StatCard label="Verified" value={stats.verified_exercises} tone="good" href="/exercises?status=approved" />
        <StatCard label="Pending review" value={stats.pending_review} tone="warn" href="/exercises?status=pending_review" />
        <StatCard label="Potential duplicates" value={stats.potential_duplicates} tone="bad" href="/review?type=duplicate_pair" />
        <StatCard label="Conflicts" value={stats.conflicts} tone="bad" href="/review?type=anatomy_conflict" />
        <StatCard label="Sources" value={stats.sources} href="/sources" hint={`${stats.sources_unknown_license} unknown license`} />
        <StatCard label="Open review items" value={stats.open_review_items} tone="warn" href="/review" />
        <StatCard label="Low confidence" value={stats.low_confidence} tone="warn" href="/exercises?confidence=0.5" />
        <StatCard label="Muscles covered" value={`${stats.muscles_covered}/${stats.muscles_total}`} tone="good" href="/coverage"
          hint={`${coveragePct}% of anatomical structures`} />
        <StatCard label="Muscles w/o exercises" value={stats.muscles_without_exercises} tone="bad" href="/coverage?filter=missing" />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <Card className="p-5">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted">By exercise type</h2>
          <Donut
            label="exercises"
            segments={stats.by_category.map((c, i) => ({
              value: c.count,
              color: CATEGORY_COLORS[i % CATEGORY_COLORS.length],
              name: c.name,
            }))}
          />
        </Card>
        <Card className="p-5">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted">By body region</h2>
          <BarList items={stats.by_region} hrefBase="/exercises?region=" />
        </Card>
        <div className="space-y-4">
          <Card className="p-5">
            <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted">Exercises by source</h2>
            <BarList items={stats.by_source.slice(0, 8)} />
          </Card>
          <Card className="p-5">
            <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">Most-covered structures</h2>
            <div className="space-y-1.5">
              {stats.top_muscles.slice(0, 8).map((m) => (
                <div key={m.slug} className="flex items-center justify-between text-sm">
                  <Link href={`/muscles/${m.slug}`} className="hover:text-brand-600 dark:hover:text-brand-400">
                    {m.name}
                  </Link>
                  <span className="text-muted">{m.count}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      <Card className="mt-4 p-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">Data quality posture</h2>
          <Link href="/datasets" className="text-xs text-brand-600 hover:underline dark:text-brand-400">
            View dataset versions & exports →
          </Link>
        </div>
        <div className="mt-3 grid gap-4 text-sm md:grid-cols-3">
          <div>
            <div className="font-medium">Provenance-first</div>
            <p className="mt-1 text-muted">
              Every aggregated record links to its source document; every key field carries an origin
              (source fact / normalized / curated / AI inference / human reviewed).
            </p>
          </div>
          <div>
            <div className="font-medium">Licensing conservative</div>
            <p className="mt-1 text-muted">
              Structured facts + links only — no copyrighted article text or media is copied. Unknown
              licenses are flagged, not assumed.
            </p>
          </div>
          <div>
            <div className="font-medium">Human review gate</div>
            <p className="mt-1 text-muted">
              Duplicates, conflicts, medical-claim language and low-confidence records queue for review
              before approval. AI enrichment is labelled and gated.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
