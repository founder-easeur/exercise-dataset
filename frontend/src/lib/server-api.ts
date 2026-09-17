/** Server-side data fetching (backend reached directly). */
import "server-only";

export const BACKEND = process.env.BACKEND_URL || "http://127.0.0.1:8000";

export async function serverGet<T>(path: string, params?: Record<string, string | number | undefined | null>): Promise<T> {
  const url = new URL(path, BACKEND);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null && v !== "") url.searchParams.set(k, String(v));
    }
  }
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`Backend ${res.status} for ${path}`);
  return res.json() as Promise<T>;
}
