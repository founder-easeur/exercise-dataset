/**
 * Regression guard: the explorer must sync the address bar with PAGE urls.
 * A past bug passed the API query path to router.replace(), so after hydration
 * the browser replaced the UI with raw JSON from /api/v1/exercises. Source
 * greps missed it once ("hollow fix"); this renders the real component and
 * asserts navigation behavior.
 */
import { fireEvent, render, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const replace = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace, push: vi.fn(), prefetch: vi.fn(), back: vi.fn() }),
  useSearchParams: () => new URLSearchParams(),
  usePathname: () => "/exercises",
}));

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    apiGet: vi.fn(async () => ({ total: 0, page: 1, page_size: 24, items: [] })),
  };
});

import ExercisesPage from "./page";

describe("exercises explorer navigation", () => {
  beforeEach(() => replace.mockClear());

  it("never navigates the browser to an API path", async () => {
    render(<ExercisesPage />);
    await waitFor(() => expect(replace).toHaveBeenCalled());
    expect(replace.mock.calls.length).toBeGreaterThan(0);
    for (const call of replace.mock.calls) {
      expect(typeof call[0]).toBe("string");
      expect(call[0].startsWith("/api/")).toBe(false);
      expect(call[0].startsWith("/exercises")).toBe(true);
    }
  });

  it("syncs filters into a shareable page URL", async () => {
    render(<ExercisesPage />);
    await waitFor(() => expect(replace).toHaveBeenCalled());
    replace.mockClear();

    const search = await waitFor(() => {
      const el = document.querySelector<HTMLInputElement>('input[placeholder*="Search"]');
      expect(el).toBeTruthy();
      return el!;
    });
    fireEvent.change(search, { target: { value: "neck stretch" } });

    await waitFor(() => expect(replace).toHaveBeenCalled());
    const url = replace.mock.calls[replace.mock.calls.length - 1][0] as string;
    expect(url.startsWith("/exercises?")).toBe(true);
    expect(url).toContain("q=neck+stretch");
    expect(url.startsWith("/api/")).toBe(false);
  });
});
