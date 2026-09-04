"use client";

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ExerciseCard } from "@/components/exercise-card";
import { Card, EmptyState, PageHeader, Pagination } from "@/components/ui";
import { apiGet, apiUrl, type ExerciseSummary } from "@/lib/api";

interface ListResponse {
  total: number;
  page: number;
  page_size: number;
  items: ExerciseSummary[];
}
interface RefItem {
  slug: string;
  name: string;
  [k: string]: unknown;
}

const STATUS_OPTIONS = [
  { value: "all", label: "All" },
  { value: "approved", label: "Approved" },
  { value: "pending_review", label: "Pending review" },
  { value: "flagged", label: "Flagged" },
  { value: "rejected", label: "Rejected" },
];

function ExercisesInner() {
  const router = useRouter();
  const params = useSearchParams();

  const [q, setQ] = useState(params.get("q") || "");
  const [filters, setFilters] = useState({
    region: params.get("region") || "",
    muscle: params.get("muscle") || "",
    muscle_group: "",
    joint: "",
    type: params.get("type") || "",
    equipment: "",
    difficulty: "",
    position: "",
    status: params.get("status") || "all",
    confidence: params.get("confidence") || "",
    source: params.get("source") || "",
    origin: "",
    sort: "name",
  });
  const [page, setPage] = useState(1);
  const [data, setData] = useState<ListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [refs, setRefs] = useState<{
    regions: RefItem[];
    muscles: RefItem[];
    groups: RefItem[];
    joints: RefItem[];
    types: RefItem[];
    equipment: RefItem[];
    sources: RefItem[];
  }>({ regions: [], muscles: [], groups: [], joints: [], types: [], equipment: [], sources: [] });

  useEffect(() => {
    Promise.all([
      apiGet<{ items: RefItem[] }>("/body-regions"),
      apiGet<{ items: RefItem[] }>("/muscles"),
      apiGet<{ items: RefItem[] }>("/joints"),
      apiGet<{ items: RefItem[] }>("/exercise-types"),
      apiGet<{ items: RefItem[] }>("/equipment"),
      apiGet<{ items: RefItem[] }>("/sources"),
    ]).then(([regions, muscles, joints, types, equipment, sources]) => {
      const groupMap = new Map<string, RefItem>();
      muscles.items.forEach((m) => {
        const g = (m as { muscle_group?: { slug: string; name: string } }).muscle_group;
        if (g) groupMap.set(g.slug, g);
      });
      setRefs({
        regions: regions.items,
        muscles: muscles.items,
        groups: [...groupMap.values()].sort((a, b) => a.name.localeCompare(b.name)),
        joints: joints.items,
        types: types.items,
        equipment: equipment.items,
        sources: sources.items,
      });
    });
  }, []);

  const query = useMemo(
    () =>
      apiUrl("/exercises", {
        q,
        body_region: filters.region,
        muscle: filters.muscle,
        muscle_group: filters.muscle_group,
        joint: filters.joint,
        type: filters.type,
        equipment: filters.equipment,
        difficulty: filters.difficulty,
        position: filters.position,
        status: filters.status,
        confidence_min: filters.confidence,
        source: filters.source,
        origin: filters.origin,
        sort: filters.sort,
        page,
        page_size: 24,
      }),
    [q, filters, page],
  );

  useEffect(() => {
    setLoading(true);
    apiGet<ListResponse>(query)
      .then(setData)
      .catch(() => setData({ total: 0, page: 1, page_size: 24, items: [] }))
      .finally(() => setLoading(false));
    router.replace(query, { scroll: false });
  }, [query, router]);

  const set = useCallback((key: string, value: string) => {
    setPage(1);
    setFilters((f) => ({ ...f, [key]: value }));
  }, []);

  function reset() {
    setQ("");
    setFilters({
      region: "", muscle: "", muscle_group: "", joint: "", type: "", equipment: "",
      difficulty: "", position: "", status: "all", confidence: "", source: "", origin: "", sort: "name",
    });
    setPage(1);
  }

  const activeFilterCount = Object.entries(filters).filter(
    ([k, v]) => v && !(k === "status" && v === "all") && !(k === "sort" && v === "name"),
  ).length + (q ? 1 : 0);

  return (
    <div>
      <PageHeader
        title="Exercise Explorer"
        subtitle={data ? `${data.total} exercises match your filters` : "Loading…"}
        actions={
          activeFilterCount > 0 ? (
            <button onClick={reset} className="rounded-lg border border-app px-3 py-1.5 text-sm hover:border-brand-400">
              Clear filters ({activeFilterCount})
            </button>
          ) : null
        }
      />

      <div className="grid gap-5 lg:grid-cols-[260px_1fr]">
        <Card className="h-fit p-4">
          <input
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
            placeholder="Search name or alias…"
            className="w-full rounded-lg border border-app bg-transparent px-3 py-2 text-sm outline-none focus:border-brand-500"
          />
          <div className="mt-4 space-y-3">
            <Select label="Body region" value={filters.region} onChange={(v) => set("region", v)}
              options={[{ value: "", label: "All regions" }, ...refs.regions.map((r) => ({ value: r.slug, label: r.name }))]} />
            <Select label="Muscle / structure" value={filters.muscle} onChange={(v) => set("muscle", v)}
              options={[{ value: "", label: "All structures" }, ...refs.muscles.map((m) => ({ value: m.slug, label: m.name }))]} />
            <Select label="Exercise type" value={filters.type} onChange={(v) => set("type", v)}
              options={[{ value: "", label: "All types" }, ...refs.types.map((t) => ({ value: t.slug, label: t.name }))]} />
            <Select label="Difficulty" value={filters.difficulty} onChange={(v) => set("difficulty", v)}
              options={[
                { value: "", label: "Any difficulty" },
                { value: "beginner", label: "Beginner" },
                { value: "intermediate", label: "Intermediate" },
                { value: "advanced", label: "Advanced" },
              ]} />
            <Select label="Equipment" value={filters.equipment} onChange={(v) => set("equipment", v)}
              options={[{ value: "", label: "Any equipment" }, ...refs.equipment.map((e) => ({ value: e.slug, label: e.name }))]} />
            <Select label="Joint" value={filters.joint} onChange={(v) => set("joint", v)}
              options={[{ value: "", label: "All joints" }, ...refs.joints.map((j) => ({ value: j.slug, label: j.name }))]} />
            <Select label="Review status" value={filters.status} onChange={(v) => set("status", v)}
              options={STATUS_OPTIONS.map((s) => ({ value: s.value, label: s.label }))} />
            <Select label="Origin" value={filters.origin} onChange={(v) => set("origin", v)}
              options={[
                { value: "", label: "All origins" },
                { value: "curated", label: "Curated" },
                { value: "aggregated", label: "Aggregated" },
              ]} />
            <Select label="Source" value={filters.source} onChange={(v) => set("source", v)}
              options={[{ value: "", label: "All sources" }, ...refs.sources.map((s) => ({ value: s.slug, label: s.name }))]} />
            <Select label="Min confidence" value={filters.confidence} onChange={(v) => set("confidence", v)}
              options={[
                { value: "", label: "Any confidence" },
                { value: "0.9", label: "≥ 90%" },
                { value: "0.75", label: "≥ 75%" },
                { value: "0.55", label: "≥ 55%" },
              ]} />
            <Select label="Sort" value={filters.sort} onChange={(v) => set("sort", v)}
              options={[
                { value: "name", label: "Name A→Z" },
                { value: "confidence", label: "Confidence ↓" },
                { value: "newest", label: "Newest first" },
              ]} />
          </div>
        </Card>

        <div>
          {loading ? (
            <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
              {Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="card h-44 animate-pulse bg-slate-100 dark:bg-slate-800/50" />
              ))}
            </div>
          ) : data && data.items.length > 0 ? (
            <>
              <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                {data.items.map((ex) => (
                  <ExerciseCard key={ex.id} ex={ex} />
                ))}
              </div>
              <div className="mt-5">
                <Pagination page={data.page} pageSize={data.page_size} total={data.total} onPage={setPage} />
              </div>
            </>
          ) : (
            <EmptyState title="No exercises found" hint="Try clearing filters or a different search term." />
          )}
        </div>
      </div>
    </div>
  );
}

function Select({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
}) {
  return (
    <label className="block">
      <span className="mb-1 block text-[11px] font-medium uppercase tracking-wide text-muted">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg border border-app bg-card px-2.5 py-1.5 text-sm outline-none focus:border-brand-500"
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function ExercisesPage() {
  return (
    <Suspense>
      <ExercisesInner />
    </Suspense>
  );
}
