import Link from "next/link";
import { notFound } from "next/navigation";
import {
  Badge, Card, ConfidenceBar, KeyValue, MedicalBadge, OriginBadge, ReviewStatusPill,
} from "@/components/ui";
import { PoseDiagram } from "@/components/pose-diagram";
import { serverGet } from "@/lib/server-api";
import type { ExerciseDetail } from "@/lib/api";

export const dynamic = "force-dynamic";

const ROLE_ORDER = ["primary", "secondary", "stabilizer", "synergist", "antagonist", "stretch_target"];
const ROLE_COLORS: Record<string, string> = {
  primary: "bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300",
  secondary: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
  stabilizer: "bg-violet-100 text-violet-700 dark:bg-violet-900/40 dark:text-violet-300",
  stretch_target: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
};
const ORIGIN_LABELS: Record<string, string> = {
  source_fact: "source fact",
  normalized: "normalized",
  curated: "curated",
  ai_inference: "AI inference",
  human_reviewed: "human reviewed",
};
const ORIGIN_STYLES: Record<string, string> = {
  source_fact: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  normalized: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
  curated: "bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300",
  ai_inference: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  human_reviewed: "bg-emerald-600 text-white",
};

export default async function ExerciseDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ research?: string }>;
}) {
  const { slug } = await params;
  const { research } = await searchParams;
  const includeResearch = research === "1";

  let ex: ExerciseDetail;
  try {
    ex = await serverGet<ExerciseDetail>(
      `/api/v1/exercises/${slug}`,
      includeResearch ? { include: "research" } : undefined,
    );
  } catch {
    notFound();
  }

  const musclesByRole = ROLE_ORDER.map((role) => ({
    role,
    items: (ex.muscles || []).filter((m) => m.role === role),
  })).filter((g) => g.items.length > 0);

  return (
    <div>
      <div className="mb-2 text-sm text-muted">
        <Link href="/exercises" className="hover:text-brand-600 dark:hover:text-brand-400">
          ← All exercises
        </Link>
      </div>

      {/* Header */}
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">{ex.name}</h1>
          <div className="mt-2 flex flex-wrap items-center gap-1.5">
            <ReviewStatusPill status={ex.review_status} />
            <OriginBadge origin={ex.origin} />
            <Badge className="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">{ex.type_name}</Badge>
            {ex.difficulty ? <Badge className="bg-slate-100 capitalize text-slate-600 dark:bg-slate-800 dark:text-slate-300">{ex.difficulty}</Badge> : null}
            {ex.is_medical_claim ? <MedicalBadge /> : null}
            {ex.aliases && ex.aliases.length > 0 ? (
              <span className="text-xs text-muted">aka {ex.aliases.slice(0, 3).join(" · ")}</span>
            ) : null}
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-muted">Extraction confidence</div>
          <div className="mt-1"><ConfidenceBar value={ex.confidence} /></div>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-3">
        {/* Main column */}
        <div className="space-y-5 lg:col-span-2">
          {ex.instructions ? (
            <Card className="p-5">
              <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">Instructions</h2>
              <ol className="space-y-2.5">
                {ex.instructions.split("\n").filter(Boolean).map((step, i) => (
                  <li key={i} className="flex gap-3 text-sm leading-relaxed">
                    <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-brand-100 text-[11px] font-semibold text-brand-700 dark:bg-brand-900/50 dark:text-brand-300">
                      {i + 1}
                    </span>
                    {step.replace(/^\d+[.)]?\s*/, "")}
                  </li>
                ))}
              </ol>
            </Card>
          ) : null}

          <div className="grid gap-5 sm:grid-cols-2">
            {ex.dosage ? (
              <Card className="p-5">
                <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted">Dosage</h2>
                <p className="text-sm leading-relaxed">{ex.dosage}</p>
              </Card>
            ) : null}
            {ex.breathing ? (
              <Card className="p-5">
                <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted">Breathing</h2>
                <p className="text-sm leading-relaxed">{ex.breathing}</p>
              </Card>
            ) : null}
            {ex.safety_notes ? (
              <Card className="p-5">
                <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted">Safety notes</h2>
                <p className="text-sm leading-relaxed">{ex.safety_notes}</p>
              </Card>
            ) : null}
            {ex.contraindications ? (
              <Card className="border-rose-200 p-5 dark:border-rose-900">
                <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-rose-600 dark:text-rose-400">
                  Contraindications
                </h2>
                <p className="text-sm leading-relaxed">{ex.contraindications}</p>
              </Card>
            ) : null}
          </div>

          {ex.clinical_relevance ? (
            <Card className="border-amber-200 p-5 dark:border-amber-900">
              <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-amber-600 dark:text-amber-400">
                Clinical relevance <Badge className="ml-1 bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">higher-risk claim</Badge>
              </h2>
              <p className="text-sm leading-relaxed">{ex.clinical_relevance}</p>
              <p className="mt-2 text-xs text-muted">
                Medical claims are recorded verbatim from clinical sources and flagged for review — never
                invented or paraphrased by the pipeline.
              </p>
            </Card>
          ) : null}

          {/* Anatomy */}
          <Card className="p-5">
            <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted">Anatomy</h2>
            {musclesByRole.map(({ role, items }) => (
              <div key={role} className="mb-3">
                <div className="mb-1.5 text-xs font-medium capitalize text-muted">{role.replace(/_/g, " ")}</div>
                <div className="flex flex-wrap gap-1.5">
                  {items.map((m) => (
                    <Link
                      key={m.slug}
                      href={`/muscles/${m.slug}`}
                      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium transition hover:opacity-80 ${ROLE_COLORS[role] || "bg-slate-100 dark:bg-slate-800"}`}
                    >
                      {m.name}
                      {m.structure_type && m.structure_type !== "muscle" ? (
                        <span className="opacity-70">· {m.structure_type}</span>
                      ) : null}
                    </Link>
                  ))}
                </div>
              </div>
            ))}
            {ex.joints && ex.joints.length > 0 ? (
              <div className="mt-4 border-t border-app pt-4">
                <div className="mb-1.5 text-xs font-medium text-muted">Joints involved</div>
                <div className="flex flex-wrap gap-1.5">
                  {ex.joints.map((j) => (
                    <span key={j.slug} className="rounded-md bg-slate-100 px-2 py-0.5 text-xs dark:bg-slate-800">
                      {j.name}
                      {j.movement ? <span className="text-muted"> · {j.movement}</span> : null}
                    </span>
                  ))}
                </div>
              </div>
            ) : null}
          </Card>

          {/* Provenance (research mode) */}
          {includeResearch && ex.provenance && ex.provenance.length > 0 ? (
            <Card className="p-5">
              <h2 className="mb-1 text-sm font-semibold uppercase tracking-wide text-muted">Provenance (research mode)</h2>
              <p className="mb-3 text-xs text-muted">
                Field-level origin tracking. AI-generated fields are always marked and require review.
              </p>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="text-muted">
                    <tr className="border-b border-app">
                      <th className="py-2 pr-4 font-medium">Field</th>
                      <th className="py-2 pr-4 font-medium">Origin</th>
                      <th className="py-2 pr-4 font-medium">Value</th>
                      <th className="py-2 pr-4 font-medium">Source / model</th>
                      <th className="py-2 font-medium">Conf.</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ex.provenance.map((p, i) => (
                      <tr key={i} className="border-b border-app last:border-0">
                        <td className="py-2 pr-4 font-medium">{p.field}</td>
                        <td className="py-2 pr-4">
                          <Badge className={ORIGIN_STYLES[p.origin] || "bg-slate-100 dark:bg-slate-800"}>
                            {ORIGIN_LABELS[p.origin] || p.origin}
                          </Badge>
                        </td>
                        <td className="max-w-[240px] truncate py-2 pr-4 text-muted" title={p.value || ""}>
                          {p.value || "—"}
                        </td>
                        <td className="py-2 pr-4">
                          {p.source_url ? (
                            <a href={p.source_url} target="_blank" rel="noreferrer" className="text-brand-600 hover:underline dark:text-brand-400">
                              {new URL(p.source_url).pathname.slice(0, 32)}…
                            </a>
                          ) : p.ai_model ? (
                            <span className="text-amber-600 dark:text-amber-400">{p.ai_model}</span>
                          ) : (
                            <span className="text-muted">internal</span>
                          )}
                        </td>
                        <td className="py-2">{p.confidence != null ? `${Math.round(p.confidence * 100)}%` : "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          ) : null}
        </div>

        {/* Sidebar */}
        <div className="space-y-5">
          {ex.media && ex.media.length > 0 ? (
            <Card className="overflow-hidden">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={ex.media[0].url} alt={`Illustration of ${ex.name}`} className="h-48 w-full object-cover" />
              <div className="px-4 py-2.5 text-[11px] leading-relaxed text-muted">
                {ex.media[0].credit}
              </div>
            </Card>
          ) : null}

          <Card className="p-5">
            <h2 className="mb-1 text-sm font-semibold uppercase tracking-wide text-muted">Movement preview</h2>
            <p className="mb-2 text-xs text-muted">
              Generated from structured data — {ex.position ? <span className="capitalize">{ex.position}</span> : "unspecified"} position
              {ex.movement_pattern ? <> · <span className="capitalize">{ex.movement_pattern}</span></> : null}. Pulsing markers show target regions.
            </p>
            <PoseDiagram
              position={ex.position}
              movement={ex.movement_pattern}
              regions={ex.body_regions.map((r) => r.slug)}
            />
          </Card>

          <Card className="p-5">
            <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">At a glance</h2>
            <KeyValue label="Body regions">
              <div className="flex flex-wrap gap-1">
                {ex.body_regions.map((r) => (
                  <Link key={r.slug} href={`/exercises?region=${r.slug}`} className="rounded-md bg-brand-50 px-2 py-0.5 text-xs text-brand-700 hover:underline dark:bg-brand-900/40 dark:text-brand-300">
                    {r.name}
                  </Link>
                ))}
              </div>
            </KeyValue>
            <KeyValue label="Equipment">
              {ex.equipment.length ? ex.equipment.join(", ") : "None (bodyweight)"}
            </KeyValue>
            <KeyValue label="Position">{ex.position ? <span className="capitalize">{ex.position}</span> : "—"}</KeyValue>
            {ex.movement_pattern ? <KeyValue label="Movement pattern"><span className="capitalize">{ex.movement_pattern}</span></KeyValue> : null}
            <KeyValue label="Review status"><ReviewStatusPill status={ex.review_status} /></KeyValue>
            <KeyValue label="Origin"><OriginBadge origin={ex.origin} /></KeyValue>
          </Card>

          <Card className="p-5">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">Sources</h2>
              <span className="text-xs text-muted">{ex.sources.length}</span>
            </div>
            {ex.sources.length === 0 ? (
              <p className="text-sm text-muted">
                {ex.origin === "curated"
                  ? "Curated reference record (no external page)."
                  : "No sources linked."}
              </p>
            ) : (
              <div className="space-y-3">
                {ex.sources.map((s, i) => (
                  <div key={i} className="rounded-lg border border-app p-3">
                    <a href={s.url} target="_blank" rel="noreferrer" className="text-sm font-medium text-brand-600 hover:underline dark:text-brand-400">
                      {s.document_title || s.source_name}
                    </a>
                    <div className="mt-1 flex flex-wrap items-center gap-1.5 text-[11px] text-muted">
                      <span className="rounded bg-slate-100 px-1.5 py-0.5 dark:bg-slate-800">{s.source_name}</span>
                      <span>{s.authority} authority</span>
                      <span>· {s.license.replace(/_/g, " ")}</span>
                      {s.attribution_required ? <span>· attribution required</span> : null}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card className="p-5">
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted">Research view</h2>
            <p className="text-xs leading-relaxed text-muted">
              Toggle field-level provenance, extraction confidence and origin for every key field of this
              record.
            </p>
            <Link
              href={`/exercises/${ex.slug}${includeResearch ? "" : "?research=1"}`}
              className="mt-3 inline-flex rounded-lg border border-app px-3 py-1.5 text-sm transition hover:border-brand-400"
            >
              {includeResearch ? "Hide provenance" : "Show provenance"}
            </Link>
          </Card>
        </div>
      </div>
    </div>
  );
}
