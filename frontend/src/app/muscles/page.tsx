"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Badge, Card, CoverageStatusBadge, EmptyState, PageHeader } from "@/components/ui";
import { apiGet, type MuscleDetail } from "@/lib/api";

interface ListResponse { total: number; items: (MuscleDetail & { body_region?: { slug: string; name: string } | null })[]; }

const STRUCTURE_ICON: Record<string, string> = {
  muscle: "🟣", tendon: "🟤", ligament: "🔴", fascia: "🟠", nerve: "🟡", joint_capsule: "⚪",
};

export default function MusclesPage() {
  const [data, setData] = useState<ListResponse | null>(null);
  const [q, setQ] = useState("");
  const [region, setRegion] = useState("");
  const [group, setGroup] = useState("");
  const [structure, setStructure] = useState("");
  const [onlySmall, setOnlySmall] = useState(false);

  useEffect(() => {
    apiGet<ListResponse>("/muscles", { page_size: 500 }).then(setData).catch(() => setData({ total: 0, items: [] }));
  }, []);

  const regions = useMemo(() => {
    const seen = new Map<string, string>();
    (data?.items || []).forEach((m) => m.body_region && seen.set(m.body_region.slug, m.body_region.name));
    return [...seen.entries()].map(([slug, name]) => ({ slug, name })).sort((a, b) => a.name.localeCompare(b.name));
  }, [data]);

  const groups = useMemo(() => {
    const seen = new Map<string, string>();
    (data?.items || []).forEach((m) => m.muscle_group && seen.set(m.muscle_group.slug, m.muscle_group.name));
    return [...seen.entries()].map(([slug, name]) => ({ slug, name })).sort((a, b) => a.name.localeCompare(b.name));
  }, [data]);

  const filtered = useMemo(() => {
    let items = data?.items || [];
    if (q) {
      const needle = q.toLowerCase();
      items = items.filter((m) =>
        m.name.toLowerCase().includes(needle) ||
        (m.aliases || []).some((a) => a.toLowerCase().includes(needle)) ||
        (m.latin_name || "").toLowerCase().includes(needle));
    }
    if (region) items = items.filter((m) => m.body_region?.slug === region);
    if (group) items = items.filter((m) => m.muscle_group?.slug === group);
    if (structure) items = items.filter((m) => m.structure_type === structure);
    if (onlySmall) items = items.filter((m) => m.is_small_overlooked);
    return items;
  }, [data, q, region, group, structure, onlySmall]);

  const structureTypes = useMemo(
    () => [...new Set((data?.items || []).map((m) => m.structure_type))].filter(Boolean).sort(),
    [data],
  );

  return (
    <div>
      <PageHeader
        title="Muscle & Structure Explorer"
        subtitle={
          data
            ? `${data.total} anatomical structures — muscles, tendons, ligaments and fascia, including small & commonly-overlooked ones`
            : "Loading…"
        }
      />

      <Card className="mb-5 p-4">
        <div className="flex flex-wrap items-center gap-3">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search name, alias or Latin name…"
            className="min-w-[220px] flex-1 rounded-lg border border-app bg-transparent px-3 py-2 text-sm outline-none focus:border-brand-500"
          />
          <select value={region} onChange={(e) => setRegion(e.target.value)} className="rounded-lg border border-app bg-card px-3 py-2 text-sm">
            <option value="">All regions</option>
            {regions.map((r) => <option key={r.slug} value={r.slug}>{r.name}</option>)}
          </select>
          <select value={group} onChange={(e) => setGroup(e.target.value)} className="rounded-lg border border-app bg-card px-3 py-2 text-sm">
            <option value="">All groups</option>
            {groups.map((g) => <option key={g.slug} value={g.slug}>{g.name}</option>)}
          </select>
          <select value={structure} onChange={(e) => setStructure(e.target.value)} className="rounded-lg border border-app bg-card px-3 py-2 text-sm">
            <option value="">All types</option>
            {structureTypes.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <label className="flex cursor-pointer items-center gap-2 text-sm">
            <input type="checkbox" checked={onlySmall} onChange={(e) => setOnlySmall(e.target.checked)} className="accent-brand-600" />
            Small / overlooked only
          </label>
        </div>
      </Card>

      {!data ? (
        <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">{Array.from({ length: 12 }).map((_, i) => (
          <div key={i} className="card h-20 animate-pulse bg-slate-100 dark:bg-slate-800/50" />))}</div>
      ) : filtered.length === 0 ? (
        <EmptyState title="No structures match" hint="Try clearing the search or filters." />
      ) : (
        <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((m) => {
            const cov = m.coverage;
            return (
              <Link key={m.slug} href={`/muscles/${m.slug}`}
                className="card flex items-center justify-between gap-3 p-3.5 transition hover:border-brand-400 dark:hover:border-brand-700">
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span title={m.structure_type}>{STRUCTURE_ICON[m.structure_type] || "⚪"}</span>
                    <span className="truncate font-medium">{m.name}</span>
                    {m.is_small_overlooked ? (
                      <Badge className="bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">small</Badge>
                    ) : null}
                  </div>
                  <div className="mt-0.5 truncate text-xs text-muted">
                    {m.body_region?.name || "—"}
                    {m.muscle_group ? ` · ${m.muscle_group.name}` : ""}
                    {m.structure_type !== "muscle" ? ` · ${m.structure_type}` : ""}
                  </div>
                </div>
                <div className="shrink-0 text-right">
                  <div className="text-sm font-semibold">{cov?.total ?? 0}</div>
                  <div className="text-[10px] text-muted">exercises</div>
                  {cov ? <div className="mt-1"><CoverageStatusBadge status={cov.status} /></div> : null}
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
