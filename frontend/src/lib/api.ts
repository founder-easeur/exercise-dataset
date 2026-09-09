/** Shared API client + domain types. */

export const API_BASE = "/api/v1";

export interface Region {
  slug: string;
  name: string;
}
export interface MuscleRef {
  slug: string;
  name: string;
  role: string;
  structure_type?: string;
}
export interface MediaRef {
  kind: string;
  url: string;
  license: string;
  credit: string;
  origin: string;
  file?: string;
  region?: string;
}
export interface SourceChip {
  slug: string;
  name: string;
  domain: string;
  url: string | null;
  authority: string;
  license: string;
  attribution_required?: boolean;
}
export interface ExerciseSummary {
  id: number;
  slug: string;
  name: string;
  aliases: string[];
  type: string;
  type_name: string;
  difficulty: string;
  position?: string | null;
  body_regions: Region[];
  primary_muscles: MuscleRef[];
  all_muscles: MuscleRef[];
  equipment: string[];
  confidence: number;
  review_status: string;
  origin: string;
  is_medical_claim: boolean;
  source_count: number;
  sources?: SourceChip[];
  media?: MediaRef[];
}
export interface SourceRef {
  source_id: number;
  source_slug: string;
  source_name: string;
  domain: string;
  source_type: string;
  authority: string;
  license: string;
  commercial_use_allowed: string;
  attribution_required: boolean;
  url: string;
  document_title?: string | null;
  retrieved_at?: string | null;
  confidence: number;
}
export interface ProvenanceRef {
  field: string;
  value?: string | null;
  origin: string;
  source_url?: string | null;
  ai_model?: string | null;
  confidence?: number | null;
  created_at?: string | null;
}
export interface ExerciseDetail extends Omit<ExerciseSummary, "sources"> {
  movement_pattern?: string | null;
  instructions?: string | null;
  breathing?: string | null;
  safety_notes?: string | null;
  contraindications?: string | null;
  clinical_relevance?: string | null;
  dosage?: string | null;
  joints: { slug: string; name: string; movement?: string | null }[];
  muscles: MuscleRef[];
  sources: SourceRef[];
  provenance?: ProvenanceRef[];
  ai_generated_fields?: string[];
}
export interface MuscleDetail {
  id: number;
  slug: string;
  name: string;
  latin_name?: string | null;
  structure_type: string;
  description?: string | null;
  is_small_overlooked: boolean;
  aliases: string[];
  body_region?: Region | null;
  muscle_group?: { slug: string; name: string } | null;
  exercise_count?: number;
  exercises?: ExerciseSummary[];
  coverage?: MuscleCoverage;
}
export interface MuscleCoverage {
  total: number;
  verified: number;
  pending: number;
  sources: number;
  stretching: number;
  mobility: number;
  rehabilitation: number;
  status: string;
}
export interface DashboardStats {
  total_exercises: number;
  verified_exercises: number;
  pending_review: number;
  curated_exercises: number;
  aggregated_exercises: number;
  low_confidence: number;
  sources: number;
  sources_unknown_license: number;
  potential_duplicates: number;
  conflicts: number;
  open_review_items: number;
  muscles_total: number;
  muscles_covered: number;
  muscles_without_exercises: number;
  by_category: { slug: string; name: string; count: number }[];
  by_region: { slug: string; name: string; count: number }[];
  by_source: { slug: string; name: string; count: number }[];
  top_muscles: { slug: string; name: string; count: number }[];
}
export interface ReviewItem {
  id: number;
  item_type: string;
  status: string;
  exercise_id?: number | null;
  exercise_name?: string | null;
  related_exercise_id?: number | null;
  related_exercise_name?: string | null;
  payload: Record<string, unknown>;
  priority: number;
  reason?: string | null;
  resolution_note?: string | null;
  created_at?: string | null;
}
export interface DuplicatePair {
  review_item_id: number;
  similarity: number;
  stage: string;
  components?: Record<string, unknown>;
  exercise_a: ExerciseSummary | null;
  exercise_b: ExerciseSummary | null;
  reason?: string | null;
}

export function apiUrl(path: string, params?: Record<string, string | number | boolean | undefined | null>) {
  const url = new URL(`${API_BASE}${path}`, "http://local");
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, String(v));
    }
  }
  return `${url.pathname}${url.search}`;
}

export async function apiGet<T>(path: string, params?: Record<string, string | number | boolean | undefined | null>): Promise<T> {
  const res = await fetch(apiUrl(path, params), { cache: "no-store" });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json() as Promise<T>;
}

export async function apiPost<T>(path: string, body: unknown, apiKey?: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(apiKey ? { "X-API-Key": apiKey } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`API ${res.status}: ${detail.slice(0, 200)}`);
  }
  return res.json() as Promise<T>;
}

export function getApiKey(): string {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem("easeur-admin-key") || "";
}
export function setApiKey(key: string) {
  window.localStorage.setItem("easeur-admin-key", key);
}
