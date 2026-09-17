/** Exercise explorer URL helpers — keep the browser URL shareable while the
 *  data fetch uses the API path. Never put API paths in router.replace(). */

export interface ExerciseFilters {
  region: string;
  muscle: string;
  muscle_group: string;
  joint: string;
  type: string;
  equipment: string;
  difficulty: string;
  position: string;
  status: string;
  confidence: string;
  source: string;
  origin: string;
  sort: string;
}

export const DEFAULT_FILTERS: ExerciseFilters = {
  region: "", muscle: "", muscle_group: "", joint: "", type: "", equipment: "",
  difficulty: "", position: "", status: "all", confidence: "", source: "",
  origin: "", sort: "name",
};

/** Page URL for the explorer (/exercises?region=neck&page=2) — shareable. */
export function buildExercisesPageUrl(q: string, filters: ExerciseFilters, page: number): string {
  const p = new URLSearchParams();
  if (q) p.set("q", q);
  for (const [key, value] of Object.entries(filters)) {
    if (!value) continue;
    if (key === "status" && value === "all") continue;
    if (key === "sort" && value === "name") continue;
    p.set(key, value);
  }
  if (page > 1) p.set("page", String(page));
  const s = p.toString();
  return s ? `/exercises?${s}` : "/exercises";
}
