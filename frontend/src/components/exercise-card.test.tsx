import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { ExerciseCard } from "@/components/exercise-card";
import type { ExerciseSummary } from "@/lib/api";

const base: ExerciseSummary = {
  id: 1,
  slug: "neck-rotation",
  name: "Neck Rotation",
  aliases: [],
  type: "mobility",
  type_name: "Mobility",
  difficulty: "beginner",
  position: "seated",
  body_regions: [{ slug: "neck", name: "Neck" }],
  primary_muscles: [
    { slug: "splenius-capitis", name: "Splenius Capitis", role: "primary" },
    { slug: "plantar-fascia", name: "Plantar Fascia", role: "primary", structure_type: "fascia" },
  ],
  all_muscles: [],
  equipment: [],
  confidence: 0.9,
  review_status: "approved",
  origin: "curated",
  is_medical_claim: false,
  source_count: 2,
};

describe("ExerciseCard", () => {
  it("renders name, region, type and status", () => {
    render(<ExerciseCard ex={base} />);
    expect(screen.getByText("Neck Rotation")).toBeInTheDocument();
    expect(screen.getByText("Neck")).toBeInTheDocument();
    expect(screen.getByText("Mobility")).toBeInTheDocument();
    expect(screen.getByText("approved")).toBeInTheDocument();
    expect(screen.getByText("90%")).toBeInTheDocument();
    expect(screen.getByText("2 sources")).toBeInTheDocument();
  });

  it("labels non-muscle structures", () => {
    render(<ExerciseCard ex={base} />);
    expect(screen.getAllByText(/fascia/).length).toBeGreaterThanOrEqual(2);
  });

  it("shows medical-claim badge only when flagged", () => {
    const { rerender } = render(<ExerciseCard ex={base} />);
    expect(screen.queryByText(/medical claim/i)).not.toBeInTheDocument();
    rerender(<ExerciseCard ex={{ ...base, is_medical_claim: true }} />);
    expect(screen.getByText(/medical claim/i)).toBeInTheDocument();
  });

  it("links to the detail page", () => {
    render(<ExerciseCard ex={base} />);
    expect(screen.getAllByRole("link")[0]).toHaveAttribute("href", "/exercises/neck-rotation");
  });
});
