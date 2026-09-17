"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Card, PageHeader } from "@/components/ui";
import { apiGet } from "@/lib/api";

interface RegionInfo {
  slug: string; name: string; description?: string | null;
  total: number; verified: number; sources: number;
  muscles_total: number; muscles_covered: number; status: string;
}

const STATUS_FILL: Record<string, string> = {
  excellent: "#10b981", good: "#6366f1", limited: "#f59e0b",
  missing: "#ef4444", needs_review: "#f97316",
};

/**
 * Simplified 2D body map. Zones are positioned on a 200x420 canvas per view;
 * front view shows anterior-dominant regions, back view posterior-dominant.
 */
const FRONT_ZONES: { slug: string; x: number; y: number; w: number; h: number; label: string; rx?: number }[] = [
  { slug: "jaw", x: 84, y: 26, w: 32, h: 22, label: "Jaw", rx: 8 },
  { slug: "neck", x: 86, y: 52, w: 28, h: 18, label: "Neck" },
  { slug: "shoulder", x: 60, y: 74, w: 80, h: 26, label: "Shoulders", rx: 12 },
  { slug: "chest", x: 72, y: 104, w: 56, h: 34, label: "Chest" },
  { slug: "elbow", x: 44, y: 140, w: 22, h: 20, label: "L", rx: 10 },
  { slug: "elbow", x: 134, y: 140, w: 22, h: 20, label: "R", rx: 10 },
  { slug: "forearm", x: 36, y: 162, w: 20, h: 44, label: "" },
  { slug: "forearm", x: 144, y: 162, w: 20, h: 44, label: "" },
  { slug: "wrist", x: 34, y: 208, w: 20, h: 12, label: "", rx: 5 },
  { slug: "wrist", x: 146, y: 208, w: 20, h: 12, label: "", rx: 5 },
  { slug: "hand", x: 32, y: 222, w: 22, h: 24, label: "", rx: 6 },
  { slug: "hand", x: 146, y: 222, w: 22, h: 24, label: "", rx: 6 },
  { slug: "hip", x: 68, y: 142, w: 64, h: 40, label: "Hips", rx: 14 },
  { slug: "knee", x: 74, y: 224, w: 22, h: 20, label: "L", rx: 9 },
  { slug: "knee", x: 104, y: 224, w: 22, h: 20, label: "R", rx: 9 },
  { slug: "calf", x: 72, y: 246, w: 24, h: 42, label: "" },
  { slug: "calf", x: 104, y: 246, w: 24, h: 42, label: "" },
  { slug: "ankle", x: 74, y: 290, w: 20, h: 14, label: "", rx: 6 },
  { slug: "ankle", x: 106, y: 290, w: 20, h: 14, label: "", rx: 6 },
  { slug: "foot", x: 72, y: 306, w: 24, h: 18, label: "", rx: 7 },
  { slug: "foot", x: 104, y: 306, w: 24, h: 18, label: "", rx: 7 },
];

const BACK_ZONES: (typeof FRONT_ZONES)[number][] = [
  { slug: "jaw", x: 84, y: 26, w: 32, h: 22, label: "Jaw", rx: 8 },
  { slug: "neck", x: 86, y: 52, w: 28, h: 18, label: "Neck" },
  { slug: "upper-back", x: 66, y: 74, w: 68, h: 32, label: "U. Back" },
  { slug: "shoulder", x: 56, y: 72, w: 26, h: 24, label: "", rx: 10 },
  { slug: "shoulder", x: 118, y: 72, w: 26, h: 24, label: "", rx: 10 },
  { slug: "lower-back", x: 72, y: 108, w: 56, h: 34, label: "L. Back" },
  { slug: "elbow", x: 44, y: 140, w: 22, h: 20, label: "L", rx: 10 },
  { slug: "elbow", x: 134, y: 140, w: 22, h: 20, label: "R", rx: 10 },
  { slug: "forearm", x: 36, y: 162, w: 20, h: 44, label: "" },
  { slug: "forearm", x: 144, y: 162, w: 20, h: 44, label: "" },
  { slug: "hand", x: 32, y: 222, w: 22, h: 24, label: "", rx: 6 },
  { slug: "hand", x: 146, y: 222, w: 22, h: 24, label: "", rx: 6 },
  { slug: "hip", x: 68, y: 142, w: 64, h: 40, label: "Glutes", rx: 14 },
  { slug: "knee", x: 74, y: 224, w: 22, h: 20, label: "L", rx: 9 },
  { slug: "knee", x: 104, y: 224, w: 22, h: 20, label: "R", rx: 9 },
  { slug: "calf", x: 72, y: 246, w: 24, h: 42, label: "" },
  { slug: "calf", x: 104, y: 246, w: 24, h: 42, label: "" },
  { slug: "ankle", x: 74, y: 290, w: 20, h: 14, label: "", rx: 6 },
  { slug: "ankle", x: 106, y: 290, w: 20, h: 14, label: "", rx: 6 },
  { slug: "foot", x: 72, y: 306, w: 24, h: 18, label: "", rx: 7 },
  { slug: "foot", x: 104, y: 306, w: 24, h: 18, label: "", rx: 7 },
];

function BodyFigure({
  title, zones, regions, onHover,
}: {
  title: string;
  zones: typeof FRONT_ZONES;
  regions: Map<string, RegionInfo>;
  onHover: (r: RegionInfo | null) => void;
}) {
  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 200 336" width="240" className="max-w-full">
        {/* silhouette */}
        <g fill="currentColor" className="text-slate-200 dark:text-slate-800">
          <circle cx="100" cy="22" r="17" />
          <rect x="84" y="50" width="32" height="20" rx="8" />
          <rect x="58" y="70" width="84" height="76" rx="20" />
          <rect x="42" y="136" width="24" height="90" rx="12" />
          <rect x="134" y="136" width="24" height="90" rx="12" />
          <rect x="30" y="222" width="26" height="28" rx="10" />
          <rect x="144" y="222" width="26" height="28" rx="10" />
          <rect x="66" y="140" width="68" height="104" rx="24" />
          <rect x="68" y="220" width="28" height="96" rx="13" />
          <rect x="104" y="220" width="28" height="96" rx="13" />
          <rect x="64" y="300" width="34" height="18" rx="8" />
          <rect x="102" y="300" width="34" height="18" rx="8" />
        </g>
        {zones.map((z, i) => {
          const info = regions.get(z.slug);
          if (!info) return null;
          return (
            <g key={`${z.slug}-${i}`}>
              <rect
                x={z.x} y={z.y} width={z.w} height={z.h} rx={z.rx ?? 6}
                fill={STATUS_FILL[info.status] || STATUS_FILL.missing}
                fillOpacity={info.total === 0 ? 0.3 : Math.min(0.9, 0.45 + info.total / 40)}
                className="cursor-pointer transition-all hover:fill-opacity-100"
                onMouseEnter={() => onHover(info)}
                onMouseLeave={() => onHover(null)}
              >
                <title>{info.name}: {info.total} exercises</title>
              </rect>
              {z.label ? (
                <text x={z.x + z.w / 2} y={z.y + z.h / 2 + 3} textAnchor="middle" fontSize="8" fontWeight="600" fill="#fff" className="pointer-events-none">
                  {z.label}
                </text>
              ) : null}
            </g>
          );
        })}
      </svg>
      <div className="mt-1 text-xs font-medium uppercase tracking-wide text-muted">{title}</div>
    </div>
  );
}

export default function BodyMapPage() {
  const [regions, setRegions] = useState<RegionInfo[] | null>(null);
  const [hovered, setHovered] = useState<RegionInfo | null>(null);

  useEffect(() => {
    apiGet<{ items: RegionInfo[] }>("/body-regions").then((d) => setRegions(d.items)).catch(() => setRegions([]));
  }, []);

  const byslug = useMemo(() => new Map((regions || []).map((r) => [r.slug, r])), [regions]);

  return (
    <div>
      <PageHeader
        title="Body Map"
        subtitle="Exercise coverage by body region — hover a region for details, click its card below to explore."
      />

      <div className="grid gap-5 lg:grid-cols-[auto_1fr]">
        <Card className="flex flex-wrap justify-center gap-8 p-6">
          <BodyFigure title="Front" zones={FRONT_ZONES} regions={byslug} onHover={setHovered} />
          <BodyFigure title="Back" zones={BACK_ZONES} regions={byslug} onHover={setHovered} />
          <div className="flex w-full flex-wrap items-center justify-center gap-4 border-t border-app pt-4 text-xs">
            {Object.entries(STATUS_FILL).map(([status, color]) => (
              <span key={status} className="flex items-center gap-1.5 capitalize text-muted">
                <span className="h-2.5 w-2.5 rounded-sm" style={{ background: color }} /> {status.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </Card>

        <div className="space-y-3">
          <Card className="min-h-[92px] p-4">
            {hovered ? (
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <div className="font-semibold">{hovered.name}</div>
                  <div className="text-sm text-muted">
                    {hovered.total} exercises ({hovered.verified} verified · {hovered.sources} with sources)
                  </div>
                </div>
                <Link
                  href={`/exercises?region=${hovered.slug}`}
                  className="rounded-lg bg-brand-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-brand-700"
                >
                  View exercises →
                </Link>
              </div>
            ) : (
              <div className="flex h-full items-center text-sm text-muted">
                Hover a region on the figure to see its coverage…
              </div>
            )}
          </Card>

          <div className="grid gap-2 sm:grid-cols-2">
            {(regions || []).map((r) => (
              <Link key={r.slug} href={`/exercises?region=${r.slug}`}
                className="card flex items-center justify-between gap-3 p-3 transition hover:border-brand-400 dark:hover:border-brand-700">
                <div>
                  <div className="text-sm font-medium">{r.name}</div>
                  <div className="text-xs text-muted">
                    {r.muscles_covered}/{r.muscles_total} structures covered
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold">{r.total}</span>
                  <span className="h-2.5 w-2.5 rounded-sm" style={{ background: STATUS_FILL[r.status] || STATUS_FILL.missing }} />
                </div>
              </Link>
            ))}
            {!regions ? <div className="card h-20 animate-pulse bg-slate-100 dark:bg-slate-800/50" /> : null}
          </div>
        </div>
      </div>
    </div>
  );
}
