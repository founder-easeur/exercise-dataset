import Link from "next/link";
import { notFound } from "next/navigation";
import { ExerciseCard } from "@/components/exercise-card";
import { Badge, Card, CoverageStatusBadge, PageHeader, StatCard } from "@/components/ui";
import { serverGet } from "@/lib/server-api";
import type { MuscleDetail } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function MuscleDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  let m: MuscleDetail;
  try {
    m = await serverGet<MuscleDetail>(`/api/v1/muscles/${slug}`);
  } catch {
    notFound();
  }

  const cov = m.coverage;

  return (
    <div>
      <div className="mb-2 text-sm text-muted">
        <Link href="/muscles" className="hover:text-brand-600 dark:hover:text-brand-400">← All structures</Link>
      </div>
      <PageHeader
        title={m.name}
        subtitle={`${m.body_region?.name || "Uncategorized"}${m.muscle_group ? ` · ${m.muscle_group.name}` : ""}${m.structure_type !== "muscle" ? ` · ${m.structure_type}` : ""}`}
        actions={
          <div className="flex items-center gap-2">
            {m.is_small_overlooked ? (
              <Badge className="bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">small / overlooked</Badge>
            ) : null}
            {cov ? <CoverageStatusBadge status={cov.status} /> : null}
          </div>
        }
      />

      <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-5">
        <StatCard label="Exercises" value={cov?.total ?? 0} tone="brand" />
        <StatCard label="Verified" value={cov?.verified ?? 0} tone="good" />
        <StatCard label="Pending review" value={cov?.pending ?? 0} tone="warn" />
        <StatCard label="Stretching" value={cov?.stretching ?? 0} />
        <StatCard label="Mobility / rehab" value={(cov?.mobility ?? 0) + (cov?.rehabilitation ?? 0)} />
      </div>

      {m.description || m.latin_name || (m.aliases && m.aliases.length) ? (
        <Card className="mb-5 p-5">
          <dl className="space-y-2 text-sm">
            {m.latin_name ? (
              <div><dt className="inline text-muted">Latin: </dt><dd className="inline italic">{m.latin_name}</dd></div>
            ) : null}
            {m.description ? <p className="leading-relaxed">{m.description}</p> : null}
            {m.aliases && m.aliases.length ? (
              <div><dt className="inline text-muted">Also known as: </dt><dd className="inline">{m.aliases.join(", ")}</dd></div>
            ) : null}
          </dl>
        </Card>
      ) : null}

      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">
        Exercises targeting this structure
      </h2>
      {m.exercises && m.exercises.length > 0 ? (
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {m.exercises.map((ex) => <ExerciseCard key={ex.id} ex={ex} />)}
        </div>
      ) : (
        <Card className="p-8 text-center text-sm text-muted">
          No exercises target this structure yet — a coverage gap. See the{" "}
          <Link href="/coverage?filter=missing" className="text-brand-600 hover:underline dark:text-brand-400">
            coverage report
          </Link>{" "}
          for gaps like this.
        </Card>
      )}
    </div>
  );
}
