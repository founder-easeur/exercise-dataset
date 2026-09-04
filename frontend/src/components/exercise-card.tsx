import Link from "next/link";
import type { ExerciseSummary } from "@/lib/api";
import { ConfidenceBar, OriginBadge, ReviewStatusPill, MedicalBadge } from "./ui";

export function ExerciseCard({ ex }: { ex: ExerciseSummary }) {
  const region = ex.body_regions[0];
  return (
    <Link
      href={`/exercises/${ex.slug}`}
      className="card group flex flex-col gap-2.5 p-4 transition hover:-translate-y-0.5 hover:border-brand-400 hover:shadow-md dark:hover:border-brand-700"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="font-medium leading-snug text-slate-900 group-hover:text-brand-700 dark:text-slate-100 dark:group-hover:text-brand-300">
          {ex.name}
        </div>
        <span className="shrink-0 rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-medium capitalize text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          {ex.type_name || ex.type}
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-1.5 text-xs text-muted">
        {region ? (
          <span className="rounded-md bg-brand-50 px-2 py-0.5 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
            {region.name}
          </span>
        ) : null}
        {ex.difficulty ? <span className="capitalize">{ex.difficulty}</span> : null}
        {ex.equipment.length === 0 ? <span>· no equipment</span> : <span>· {ex.equipment.join(", ")}</span>}
      </div>
      <div className="flex flex-wrap gap-1.5">
        {ex.primary_muscles.slice(0, 3).map((m) => (
          <span key={m.slug} className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] dark:bg-slate-800">
            {m.name}
            {m.structure_type && m.structure_type !== "muscle" ? (
              <span className="text-muted"> ({m.structure_type})</span>
            ) : null}
          </span>
        ))}
        {ex.primary_muscles.length > 3 ? (
          <span className="text-[11px] text-muted">+{ex.primary_muscles.length - 3} more</span>
        ) : null}
      </div>
      <div className="mt-auto flex items-center justify-between gap-2 pt-1">
        <div className="flex items-center gap-1.5">
          <ReviewStatusPill status={ex.review_status} />
          <OriginBadge origin={ex.origin} />
          {ex.is_medical_claim ? <MedicalBadge /> : null}
        </div>
        <div className="flex items-center gap-2">
          {ex.source_count > 1 ? (
            <span className="text-[11px] text-muted" title="Sources describing this exercise">
              {ex.source_count} sources
            </span>
          ) : null}
          <ConfidenceBar value={ex.confidence} />
        </div>
      </div>
    </Link>
  );
}
