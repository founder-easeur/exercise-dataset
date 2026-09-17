import { describe, expect, it } from "vitest";
import { apiUrl } from "@/lib/api";

describe("apiUrl", () => {
  it("builds paths with params", () => {
    expect(apiUrl("/exercises", { page: 2, page_size: 24 })).toBe("/api/v1/exercises?page=2&page_size=24");
  });
  it("drops empty/undefined params", () => {
    expect(apiUrl("/exercises", { q: "", region: undefined, muscle: null, status: "all" }))
      .toBe("/api/v1/exercises?status=all");
  });
  it("encodes values"  , () => {
    expect(apiUrl("/exercises", { q: "low back & knee" })).toBe("/api/v1/exercises?q=low+back+%26+knee");
  });
});
