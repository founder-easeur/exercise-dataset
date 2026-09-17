import Link from "next/link";
import type { ExerciseSummary, SourceChip } from "@/lib/api";
import { ConfidenceBar, OriginBadge, ReviewStatusPill, MedicalBadge } from "./ui";

/** Clickable source attribution chips (direct links to the original pages). */
export function SourceChips({ sources, max = 3 }: { sources?: SourceChip[]; max?: number }) {
  if (!sources || sources.length === 0) return null;
  const shown = sources.slice(0, max);
  return (
    <div className="flex flex-wrap items-center gap-1.5">
      {shown.map((s) =>
        s.url ? (
          <a
            key={`${s.slug}-${s.url}`}
            href={s.url}
            target="_blank"
            rel="noreferrer"
            title={`${s.name} — ${s.license.replace(/_/g, " ")} license · ${s.authority} authority. Opens the original page.`}
            className="relative z-10 inline-flex max-w-[170px] items-center gap-1 rounded-md border border-app bg-card px-1.5 py-0.5 text-[11px] text-muted transition hover:border-brand-400 hover:text-brand-600 dark:hover:border-brand-600 dark:hover:text-brand-400"
          >
            <span
              className={`h-1.5 w-1.5 shrink-0 rounded-full ${
                s.authority === "high" ? "bg-emerald-500" : "bg-amber-500"
              }`}
              title={`${s.authority} authority`}
            />
            <span className="truncate">{s.domain.replace(/^www\./, "")}</span>
            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" className="shrink-0 opacity-60">
              <path d="M7 17 17 7M9 7h8v8" />
            </svg>
          </a>
        ) : null,
      )}
      {sources.length > max ? (
        <span className="text-[11px] text-muted">+{sources.length - max} more</span>
      ) : null}
    </div>
  );
}

export function ExerciseCard({ ex }: { ex: ExerciseSummary }) {
  const region = ex.body_regions[0];
  const image = ex.media?.[0];
  return (
    <div className="card group relative flex flex-col overflow-hidden transition hover:-translate-y-0.5 hover:border-brand-400 hover:shadow-md dark:hover:border-brand-700">
      {/* Whole-card link overlay — keeps HTML valid (no nested anchors) while
          source chips below sit above it with relative z-10. */}
      <Link
        href={`/exercises/${ex.slug}`}
        className="absolute inset-0 z-0"
        aria-label={`View ${ex.name}`}
      />
      {image ? (
        <div className="relative h-28 w-full overflow-hidden bg-brand-50 dark:bg-brand-900/20">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={image.url}
            alt={`Illustration of ${ex.name}`}
            loading="lazy"
            className="h-full w-full object-cover transition duration-300 group-hover:scale-[1.03]"
          />
          <span className="absolute bottom-1.5 right-1.5 rounded-md bg-white/85 px-1.5 py-0.5 text-[10px] font-medium text-slate-600 backdrop-blur dark:bg-slate-900/80 dark:text-slate-300">
            AI illustration
          </span>
        </div>
      ) : null}
      <div className="flex flex-1 flex-col gap-2.5 p-4">
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

        {/* Source attribution — direct links so users can verify the origin */}
        {ex.sources && ex.sources.length > 0 ? (
          <div className="relative z-10">
            <div className="mb-1 text-[10px] font-medium uppercase tracking-wide text-muted">Source</div>
            <SourceChips sources={ex.sources} />
          </div>
        ) : ex.origin === "curated" ? (
          <div className="text-[11px] text-muted">Curated by Easeur editorial team</div>
        ) : null}

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
      </div>
    </div>
  );
}
