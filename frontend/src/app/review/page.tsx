"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { Badge, Card, ConfidenceBar, EmptyState, PageHeader } from "@/components/ui";
import { apiGet, apiPost, getApiKey, setApiKey, type DuplicatePair, type ReviewItem } from "@/lib/api";

type Tab = "duplicates" | "queue" | "conflicts";

interface ConflictRow {
  id: number; field: string; exercise_id: number; exercise_name?: string;
  value_a: string; value_b: string; source_a?: string; source_b?: string; status: string;
}

const TYPE_LABELS: Record<string, string> = {
  duplicate_pair: "Duplicate pair",
  low_confidence: "Low confidence",
  missing_anatomy: "Missing anatomy",
  missing_source: "Missing source",
  licensing_unknown: "Unknown licensing",
  medical_claim: "Medical claim",
  anatomy_conflict: "Anatomy conflict",
  data_gap: "Data gap",
};

export default function ReviewPage() {
  const [tab, setTab] = useState<Tab>("duplicates");
  const [apiKey, setKey] = useState("");
  const [keyDraft, setKeyDraft] = useState("");
  const [pairs, setPairs] = useState<DuplicatePair[]>([]);
  const [items, setItems] = useState<ReviewItem[]>([]);
  const [itemType, setItemType] = useState("");
  const [conflicts, setConflicts] = useState<ConflictRow[]>([]);
  const [busy, setBusy] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [notes, setNotes] = useState<Record<number, string>>({});
  const [resolved, setResolved] = useState<Record<number, string>>({});

  useEffect(() => setKey(getApiKey()), []);

  const reload = useCallback(() => {
    apiGet<{ items: DuplicatePair[] }>("/duplicates").then((d) => setPairs(d.items)).catch(() => setPairs([]));
    apiGet<{ items: ReviewItem[] }>("/review", { status: "open", item_type: itemType || undefined, limit: 200 })
      .then((d) => setItems(d.items)).catch(() => setItems([]));
    apiGet<{ items: ConflictRow[] }>("/conflicts").then((d) => setConflicts(d.items)).catch(() => setConflicts([]));
  }, [itemType]);

  useEffect(reload, [reload]);

  async function act(itemId: number, action: string, edits?: Record<string, unknown>) {
    setBusy(itemId);
    setError("");
    try {
      await apiPost(`/review/${itemId}/action`, { action, note: notes[itemId] || undefined, edits }, apiKey);
      setResolved((r) => ({ ...r, [itemId]: action }));
      setTimeout(reload, 400);
    } catch (e) {
      setError(e instanceof Error ? e.message : "action failed");
    } finally {
      setBusy(null);
    }
  }

  if (!apiKey) {
    return (
      <div>
        <PageHeader title="Review Queue" subtitle="Admin key required to review records." />
        <Card className="mx-auto max-w-md p-6">
          <label className="mb-2 block text-sm font-medium">Admin API key</label>
          <input
            type="password"
            value={keyDraft}
            onChange={(e) => setKeyDraft(e.target.value)}
            placeholder="X-API-Key"
            className="w-full rounded-lg border border-app bg-transparent px-3 py-2 text-sm outline-none focus:border-brand-500"
            onKeyDown={(e) => { if (e.key === "Enter" && keyDraft) { setApiKey(keyDraft); setKey(keyDraft); } }}
          />
          <p className="mt-2 text-xs text-muted">
            The key is stored locally in your browser only and sent as <code>X-API-Key</code> with review
            actions. Default dev key: <code>dev-admin-key</code>.
          </p>
          <button
            onClick={() => { setApiKey(keyDraft); setKey(keyDraft); }}
            disabled={!keyDraft}
            className="mt-4 w-full rounded-lg bg-brand-600 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:opacity-40"
          >
            Unlock review tools
          </button>
        </Card>
      </div>
    );
  }

  const tabs: { id: Tab; label: string; count: number }[] = [
    { id: "duplicates", label: "Duplicate pairs", count: pairs.length },
    { id: "queue", label: "Review queue", count: items.length },
    { id: "conflicts", label: "Conflicts", count: conflicts.length },
  ];

  return (
    <div>
      <PageHeader
        title="Review Queue"
        subtitle="Human review gate: duplicates, conflicts, low-confidence and medical-claim records. Every decision is audit-logged."
        actions={
          <button onClick={() => { setApiKey(""); setKey(""); }}
            className="rounded-lg border border-app px-3 py-1.5 text-sm hover:border-brand-400">
            Lock 🔒
          </button>
        }
      />

      {error ? <div className="mb-4 rounded-lg bg-rose-100 px-4 py-2 text-sm text-rose-700 dark:bg-rose-900/40 dark:text-rose-300">{error}</div> : null}

      <div className="mb-4 flex flex-wrap items-center gap-2">
        <div className="flex rounded-lg border border-app p-0.5">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`rounded-md px-3 py-1.5 text-sm ${tab === t.id ? "bg-brand-600 text-white" : ""}`}>
              {t.label} <span className="opacity-70">({t.count})</span>
            </button>
          ))}
        </div>
        {tab === "queue" ? (
          <select value={itemType} onChange={(e) => setItemType(e.target.value)}
            className="rounded-lg border border-app bg-card px-3 py-2 text-sm">
            <option value="">All item types</option>
            {Object.entries(TYPE_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
          </select>
        ) : null}
      </div>

      {tab === "duplicates" ? (
        pairs.length === 0 ? (
          <EmptyState title="No open duplicate pairs" hint="Dedup runs after every aggregation; uncertain matches always land here, never auto-merged." />
        ) : (
          <div className="space-y-4">
            {pairs.map((p) => (
              <DuplicatePairCard key={p.review_item_id} p={p} busy={busy === p.review_item_id}
                resolved={resolved[p.review_item_id]} note={notes[p.review_item_id] || ""}
                onNote={(n) => setNotes((s) => ({ ...s, [p.review_item_id]: n }))}
                onAct={(a, edits) => act(p.review_item_id, a, edits)} />
            ))}
          </div>
        )
      ) : null}

      {tab === "queue" ? (
        items.length === 0 ? (
          <EmptyState title="Queue is empty" hint="Run validation to sweep for low-confidence, unlicensed or medical-claim records." />
        ) : (
          <div className="space-y-2">
            {items.map((i) => (
              <Card key={i.id} className="p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <Badge className="bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
                        {TYPE_LABELS[i.item_type] || i.item_type}
                      </Badge>
                      {i.exercise_name ? (
                        <Link href={`/exercises/${i.exercise_id}`} className="text-sm font-medium hover:text-brand-600 dark:hover:text-brand-400">
                          {i.exercise_name}
                        </Link>
                      ) : null}
                      {i.priority >= 3 ? <Badge className="bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300">high</Badge> : null}
                    </div>
                    <div className="mt-1 text-xs text-muted">
                      {i.reason || JSON.stringify(i.payload).slice(0, 120)}
                    </div>
                  </div>
                  <div className="flex flex-wrap items-center gap-1.5">
                    {resolved[i.id] ? (
                      <Badge className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300">✓ {resolved[i.id]}</Badge>
                    ) : (
                      <>
                        <ActionBtn onClick={() => act(i.id, "approve")} disabled={busy === i.id} tone="good">Approve</ActionBtn>
                        <ActionBtn onClick={() => act(i.id, "reject")} disabled={busy === i.id} tone="bad">Reject</ActionBtn>
                        <ActionBtn onClick={() => act(i.id, "flag")} disabled={busy === i.id} tone="warn">Flag</ActionBtn>
                        <ActionBtn onClick={() => act(i.id, "dismiss")} disabled={busy === i.id}>Dismiss</ActionBtn>
                      </>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )
      ) : null}

      {tab === "conflicts" ? (
        conflicts.length === 0 ? (
          <EmptyState title="No recorded conflicts" hint="When two trusted sources disagree on a field, the conflict is recorded — never silently resolved." />
        ) : (
          <div className="space-y-2">
            {conflicts.map((c) => (
              <Card key={c.id} className="p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <div className="text-sm font-medium">
                      <code>{c.field}</code> on{" "}
                      <Link href={`/exercises/${c.exercise_id}`} className="text-brand-600 hover:underline dark:text-brand-400">
                        exercise #{c.exercise_id}
                      </Link>
                    </div>
                    <div className="mt-1.5 grid gap-1 text-xs sm:grid-cols-2">
                      <div className="rounded-md bg-slate-100 p-2 dark:bg-slate-800">
                        <div className="mb-0.5 text-muted">{c.source_a || "source A"}</div>
                        <code className="break-all">{c.value_a}</code>
                      </div>
                      <div className="rounded-md bg-slate-100 p-2 dark:bg-slate-800">
                        <div className="mb-0.5 text-muted">{c.source_b || "source B"}</div>
                        <code className="break-all">{c.value_b}</code>
                      </div>
                    </div>
                  </div>
                  <Badge className="bg-amber-100 capitalize text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">{c.status}</Badge>
                </div>
              </Card>
            ))}
          </div>
        )
      ) : null}
    </div>
  );
}

function ActionBtn({ children, onClick, disabled, tone = "default" }: {
  children: React.ReactNode; onClick: () => void; disabled?: boolean; tone?: "default" | "good" | "bad" | "warn";
}) {
  const tones = {
    default: "border-app hover:border-brand-400",
    good: "border-emerald-300 text-emerald-700 hover:bg-emerald-50 dark:border-emerald-800 dark:text-emerald-300 dark:hover:bg-emerald-900/20",
    bad: "border-rose-300 text-rose-700 hover:bg-rose-50 dark:border-rose-800 dark:text-rose-300 dark:hover:bg-rose-900/20",
    warn: "border-amber-300 text-amber-700 hover:bg-amber-50 dark:border-amber-800 dark:text-amber-300 dark:hover:bg-amber-900/20",
  };
  return (
    <button onClick={onClick} disabled={disabled}
      className={`rounded-lg border px-3 py-1.5 text-xs font-medium transition disabled:opacity-40 ${tones[tone]}`}>
      {children}
    </button>
  );
}

function DuplicatePairCard({
  p, busy, resolved, note, onNote, onAct,
}: {
  p: DuplicatePair; busy: boolean; resolved?: string; note: string;
  onNote: (n: string) => void; onAct: (a: string, edits?: Record<string, unknown>) => void;
}) {
  const [keep, setKeep] = useState<"a" | "b">("a");
  const a = p.exercise_a;
  const b = p.exercise_b;
  const sim = Math.round((p.similarity || 0) * 100);
  const comp = p.components as Record<string, number> | undefined;

  return (
    <Card className="p-5">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <Badge className="bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">{p.stage} match</Badge>
          <span className="text-sm font-semibold">{sim}% similar</span>
          {comp ? (
            <span className="text-xs text-muted">
              name {Math.round((comp.name || 0) * 100)}% · anatomy {Math.round((comp.anatomy || 0) * 100)}% · category {Math.round((comp.category || 0) * 100)}%
            </span>
          ) : null}
        </div>
        {resolved ? (
          <Badge className="bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300">✓ {resolved}</Badge>
        ) : null}
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        {[a, b].map((ex, idx) => (
          ex ? (
            <div key={idx} className={`rounded-xl border-2 p-4 transition ${
              !resolved && ((idx === 0 && keep === "a") || (idx === 1 && keep === "b"))
                ? "border-brand-500 bg-brand-50/50 dark:bg-brand-900/10"
                : "border-app"}`}>
              <div className="mb-1 flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wide text-muted">
                  {idx === 0 ? "A" : "B"} · {ex.origin} · {ex.review_status.replace(/_/g, " ")}
                </span>
                {!resolved ? (
                  <label className="flex cursor-pointer items-center gap-1 text-[11px] text-muted">
                    <input type="radio" name={`keep-${p.review_item_id}`} checked={(idx === 0) === (keep === "a")}
                      onChange={() => setKeep(idx === 0 ? "a" : "b")} className="accent-brand-600" />
                    keep
                  </label>
                ) : null}
              </div>
              <Link href={`/exercises/${ex.slug}`} className="font-medium hover:text-brand-600 dark:hover:text-brand-400">
                {ex.name}
              </Link>
              <div className="mt-2 space-y-1 text-xs text-muted">
                <div>Type: {ex.type_name || ex.type} · {ex.difficulty}</div>
                <div>Regions: {ex.body_regions.map((r) => r.name).join(", ") || "—"}</div>
                <div>Muscles: {ex.all_muscles.map((m) => m.name).slice(0, 4).join(", ") || "—"}</div>
                <div>Equipment: {ex.equipment.join(", ") || "none"}</div>
                <div className="flex items-center gap-2 pt-1">
                  <ConfidenceBar value={ex.confidence} />
                  {ex.source_count > 0 ? <span>· {ex.source_count} sources</span> : null}
                </div>
              </div>
            </div>
          ) : (
            <div key={idx} className="rounded-xl border border-app p-4 text-sm text-muted">Record no longer exists.</div>
          )
        ))}
      </div>

      {!resolved ? (
        <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-app pt-4">
          <input value={note} onChange={(e) => onNote(e.target.value)} placeholder="Optional decision note (audit-logged)…"
            className="min-w-[200px] flex-1 rounded-lg border border-app bg-transparent px-3 py-2 text-sm outline-none focus:border-brand-500" />
          <ActionBtn onClick={() => onAct("merge", { keep: keep === "a" ? "primary" : "related" })} disabled={busy} tone="good">
            Merge → keep {keep.toUpperCase()}
          </ActionBtn>
          <ActionBtn onClick={() => onAct("dismiss")} disabled={busy}>Keep both</ActionBtn>
        </div>
      ) : null}
      {p.reason ? <div className="mt-2 text-xs text-muted">Why queued: {p.reason}</div> : null}
    </Card>
  );
}
