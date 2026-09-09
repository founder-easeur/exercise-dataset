import { describe, expect, it } from "vitest";
import { buildExercisesPageUrl, DEFAULT_FILTERS } from "@/lib/exercise-filters";

describe("buildExercisesPageUrl", () => {
  it("returns the bare page path for default state", () => {
    expect(buildExercisesPageUrl("", DEFAULT_FILTERS, 1)).toBe("/exercises");
  });

  it("includes non-default filters and search", () => {
    const url = buildExercisesPageUrl("stretch", { ...DEFAULT_FILTERS, region: "neck", type: "stretching" }, 1);
    expect(url).toBe("/exercises?q=stretch&region=neck&type=stretching");
  });

  it("omits default status/sort values", () => {
    const url = buildExercisesPageUrl("", DEFAULT_FILTERS, 1);
    expect(url).not.toContain("status");
    expect(url).not.toContain("sort");
  });

  it("adds the page param only beyond page 1", () => {
    expect(buildExercisesPageUrl("", DEFAULT_FILTERS, 3)).toBe("/exercises?page=3");
    expect(buildExercisesPageUrl("", DEFAULT_FILTERS, 2)).toContain("page=2");
  });

  it("never produces an API path", () => {
    const url = buildExercisesPageUrl("x", { ...DEFAULT_FILTERS, status: "approved" }, 5);
    expect(url.startsWith("/api/")).toBe(false);
    expect(url.startsWith("/exercises")).toBe(true);
  });
});
