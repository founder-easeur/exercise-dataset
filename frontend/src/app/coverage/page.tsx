"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { Badge, Card, CoverageStatusBadge, PageHeader, StatCard } from "@/components/ui";
import { apiGet } from "@/lib/api";

interface MuscleCoverageRow {
  id: number; slug: string; name: string; structure_type: string; is_small_overlooked: boolean;
  region_slug: string; region_name: string;
  total: number; verified: number; pending: number; sources: number;
  stretching: number; mobility: number; rehabilitation: number; status: string;
}
interface CoverageResponse {
  total: number;
  summary: { missing: number; limited: number; good: number; excellent: number; needs_review: number };
  items: MuscleCoverageRow[];
}
interface RegionRow {
  slug: string; name: string; total: number; verified: number; sources: number;
  muscles_total: number; muscles_covered: number; status: string;
}

function CoverageInner() {
  const params = useSearchParams();
  const [tab, setTab] = useState<"muscles" | "regions">(params.get("tab") === "regions" ? "regions" : "muscles");
  const [filter, setFilter] = useState(params.get("filter") || "");
  const [q, setQ] = useState("");
  const [data, setData] = useState<CoverageResponse | null>(null);
  const [regions, setRegions] = useState<RegionRow[] | null>(null);
  const [onlySmall, setOnlySmall] = useState(false);

  useEffect(() => {
    apiGet<CoverageResponse>("/stats/coverage/muscles").then(setData).catch(() =>
      setData({ total: 0, summary: { missing: 0, limited: 0, good: 0, excellent: 0, needs_review: 0 }, items: [] }));
    apiGet<{ items: RegionRow[] }>("/body-regions").then((d) => setRegions(d.items)).catch(() => setRegions([]));
  }, []);

  const muscles = useMemo(() => {
    let items = data?.items || [];
    if (filter) items = items.filter((m) => m.status === filter);
    if (onlySmall) items = items.filter((m) => m.is_small_overlooked);
    if (q) {
      const needle = q.toLowerCase();
      items = items.filter((m) => m.name.toLowerCase().includes(needle) || m.region_name.toLowerCase().includes(needle));
    }
    return items;
  }, [data, filter, q, onlySmall]);

  const regionGaps = useMemo(
    () => (regions || []).filter((r) => r.muscles_covered < r.muscles_total),
    [regions],
  );

  return (
    <div>
      <PageHeader
        title="Coverage Analysis"
        subtitle="Which anatomical structures and regions have exercise coverage — and where the gaps are."
      />

      <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-5">
        <StatCard label="Excellent" value={data?.summary.excellent ?? "…"} tone="good" />
        <StatCard label="Good" value={data?.summary.good ?? "…"} tone="brand" />
        <StatCard label="Limited" value={data?.summary.limited ?? "…"} tone="warn" />
        <StatCard label="Missing" value={data?.summary.missing ?? "…"} tone="bad" />
        <StatCard label="Needs review" value={data?.summary.needs_review ?? "…"} tone="warn" />
      </div>

      <div className="mb-4 flex flex-wrap items-center gap-2">
        <div className="flex rounded-lg border border-app p-0.5">
          <button onClick={() => setTab("muscles")}
            className={`rounded-md px-3 py-1.5 text-sm ${tab === "muscles" ? "bg-brand-600 text-white" : ""}`}>
            Muscle / structure coverage
          </button>
          <button onClick={() => setTab("regions")}
            className={`rounded-md px-3 py-1.5 text-sm ${tab === "regions" ? "bg-brand-600 text-white" : ""}`}>
            Region gaps
          </button>
        </div>
        {tab === "muscles" ? (
          <>
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search structure or region…"
              className="min-w-[200px] flex-1 rounded-lg border border-app bg-transparent px-3 py-2 text-sm outline-none focus:border-brand-500" />
            <select value={filter} onChange={(e) => setFilter(e.target.value)}
              className="rounded-lg border border-app bg-card px-3 py-2 text-sm">
              <option value="">All statuses</option>
              <option value="excellent">Excellent</option>
              <option value="good">Good</option>
              <option value="limited">Limited</option>
              <option value="missing">Missing</option>
              <option value="needs_review">Needs review</option>
            </select>
            <label className="flex cursor-pointer items-center gap-2 text-sm">
              <input type="checkbox" checked={onlySmall} onChange={(e) => setOnlySmall(e.target.checked)} className="accent-brand-600" />
              Small / overlooked
            </label>
          </>
        ) : null}
      </div>

      {tab === "muscles" ? (
        <Card className="overflow-x-auto p-0">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-app text-xs uppercase tracking-wide text-muted">
              <tr>
                <th className="px-4 py-3 font-medium">Structure</th>
                <th className="px-4 py-3 font-medium">Region</th>
                <th className="px-4 py-3 font-medium">Type</th>
                <th className="px-4 py-3 text-right font-medium">Exercises</th>
                <th className="px-4 py-3 text-right font-medium">Verified</th>
                <th className="px-4 py-3 text-right font-medium">Sources</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {muscles.map((m) => (
                <tr key={m.slug} className="border-b border-app last:border-0 hover:bg-brand-50/50 dark:hover:bg-brand-900/10">
                  <td className="px-4 py-2.5">
                    <Link href={`/muscles/${m.slug}`} className="font-medium hover:text-brand-600 dark:hover:text-brand-400">
                      {m.name}
                    </Link>
                    {m.is_small_overlooked ? (
                      <Badge className="ml-2 bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">small</Badge>
                    ) : null}
                  </td>
                  <td className="px-4 py-2.5 text-muted">{m.region_name}</td>
                  <td className="px-4 py-2.5 text-muted">{m.structure_type}</td>
                  <td className="px-4 py-2.5 text-right font-medium">{m.total}</td>
                  <td className="px-4 py-2.5 text-right text-muted">{m.verified}</td>
                  <td className="px-4 py-2.5 text-right text-muted">{m.sources}</td>
                  <td className="px-4 py-2.5"><CoverageStatusBadge status={m.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
          {!data ? <div className="p-8 text-center text-sm text-muted">Loading…</div> : null}
        </Card>
      ) : (
        <div className="space-y-3">
          {regionGaps.length === 0 ? (
            <Card className="p-8 text-center text-sm text-muted">All regions fully covered.</Card>
          ) : (
            regionGaps.map((r) => {
              const pct = Math.round((r.muscles_covered / Math.max(1, r.muscles_total)) * 100);
              return (
                <Link key={r.slug} href={`/exercises?region=${r.slug}`}
                  className="card flex items-center gap-4 p-4 transition hover:border-brand-400 dark:hover:border-brand-700">
                  <div className="w-32 font-medium">{r.name}</div>
                  <div className="h-3 flex-1 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                    <div className="h-full rounded-full bg-brand-500" style={{ width: `${pct}%` }} />
                  </div>
                  <div className="w-40 text-right text-sm text-muted">
                    {r.muscles_covered}/{r.muscles_total} structures · {pct}%
                  </div>
                  <div className="w-24 text-right text-sm font-medium">{r.total} exercises</div>
                </Link>
              );
            })
          )}
          {regions && regions.length > 0 ? (
            <p className="text-xs text-muted">
              {regions.length - regionGaps.length} of {regions.length} regions have complete structure coverage.
            </p>
          ) : null}
        </div>
      )}
    </div>
  );
}

export default function CoveragePage() {
  return (
    <Suspense>
      <CoverageInner />
    </Suspense>
  );
}
