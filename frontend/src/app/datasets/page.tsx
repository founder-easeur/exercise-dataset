"use client";

import { useEffect, useState } from "react";
import { Badge, Card, PageHeader } from "@/components/ui";
import { apiGet } from "@/lib/api";

interface Version {
  id: number; version: string; label?: string | null; notes?: string | null;
  created_at?: string | null; exercise_count: number; approved_count: number;
  muscles_count: number; sources_count: number; content_hash?: string | null;
}

const EXPORTS = [
  { dataset: "exercises", label: "Exercises", desc: "Full exercise records with anatomy, instructions, dosage, sources and confidence." },
  { dataset: "muscles", label: "Muscles & structures", desc: "Anatomy taxonomy: 121 structures incl. tendons, ligaments and fascia with coverage stats." },
  { dataset: "body-regions", label: "Body regions", desc: "16 regions with per-region exercise and structure coverage." },
];
const FORMATS = ["json", "jsonl", "csv"];

export default function DatasetsPage() {
  const [versions, setVersions] = useState<Version[] | null>(null);

  useEffect(() => {
    apiGet<{ items: Version[] }>("/datasets").then((d) => setVersions(d.items)).catch(() => setVersions([]));
  }, []);

  return (
    <div>
      <PageHeader
        title="Datasets & Versions"
        subtitle="Immutable snapshots of the knowledge base. EaseurWorkout and any future consumers read these exports via the public API — never the database directly."
      />

      <Card className="mb-5 p-5">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">Current exports</h2>
        <div className="space-y-2">
          {EXPORTS.map((e) => (
            <div key={e.dataset} className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-app p-3">
              <div className="min-w-[220px] flex-1">
                <div className="text-sm font-medium">{e.label} <code className="text-xs text-muted">{e.dataset}</code></div>
                <div className="text-xs text-muted">{e.desc}</div>
              </div>
              <div className="flex gap-1.5">
                {FORMATS.map((f) => (
                  <a key={f} href={`/api/v1/export?dataset=${e.dataset}&fmt=${f}`}
                    className="rounded-lg border border-app px-2.5 py-1 text-xs font-medium uppercase transition hover:border-brand-400 hover:text-brand-600 dark:hover:text-brand-400">
                    {f}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card className="p-5">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">Version history</h2>
          <span className="text-xs text-muted">snapshots are content-hashed</span>
        </div>
        {versions === null ? (
          <div className="h-16 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800/50" />
        ) : versions.length === 0 ? (
          <p className="text-sm text-muted">No versions snapshotted yet.</p>
        ) : (
          <div className="space-y-3">
            {versions.map((v) => (
              <div key={v.id} className="rounded-lg border border-app p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="rounded-lg bg-brand-600 px-2.5 py-1 text-sm font-semibold text-white">{v.version}</span>
                    <span className="font-medium">{v.label || "—"}</span>
                  </div>
                  <span className="text-xs text-muted">
                    {v.created_at ? new Date(v.created_at).toLocaleString() : ""}
                  </span>
                </div>
                {v.notes ? <p className="mt-2 text-sm text-muted">{v.notes}</p> : null}
                <div className="mt-2 flex flex-wrap gap-1.5">
                  <Badge className="bg-slate-100 dark:bg-slate-800">{v.exercise_count} exercises</Badge>
                  <Badge className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300">{v.approved_count} approved</Badge>
                  <Badge className="bg-slate-100 dark:bg-slate-800">{v.muscles_count} structures</Badge>
                  <Badge className="bg-slate-100 dark:bg-slate-800">{v.sources_count} sources</Badge>
                  {v.content_hash ? (
                    <code className="text-[10px] text-muted">{v.content_hash.slice(0, 16)}…</code>
                  ) : null}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      <Card className="mt-5 p-5 text-sm leading-relaxed text-muted">
        <strong className="text-slate-900 dark:text-slate-100">Consumer contract.</strong> The public
        REST API (<code>/api/v1/*</code>, OpenAPI docs at <code>/docs</code>) is the only supported
        access path. By default it serves <em>approved</em> exercises only; research endpoints expose
        pending records and provenance for review tooling. Dataset versions let consumers pin a stable
        snapshot while aggregation continues.
      </Card>
    </div>
  );
}
