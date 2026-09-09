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

  it("shows the illustration thumbnail when media is present", () => {
    const { rerender } = render(
      <ExerciseCard ex={{ ...base, media: [{ kind: "illustration", url: "/static/exercises/neck.png", license: "ai-generated", credit: "AI-generated", origin: "generated" }] }} />,
    );
    const img = screen.getByAltText("Illustration of Neck Rotation") as HTMLImageElement;
    expect(img).toBeInTheDocument();
    expect(img.src).toContain("/static/exercises/neck.png");
    rerender(<ExerciseCard ex={base} />);
    expect(screen.queryByAltText("Illustration of Neck Rotation")).not.toBeInTheDocument();
  });

  it("labels non-muscle structures", () => {
    render(<ExerciseCard ex={base} />);
    expect(screen.getByText(/Plantar Fascia/)).toBeInTheDocument();
    expect(screen.getByText(/fascia/)).toBeInTheDocument(); // structure type annotated on chip
  });

  it("shows medical-claim badge only when flagged", () => {
    const { rerender } = render(<ExerciseCard ex={base} />);
    expect(screen.queryByText(/medical claim/i)).not.toBeInTheDocument();
    rerender(<ExerciseCard ex={{ ...base, is_medical_claim: true }} />);
    expect(screen.getByText(/medical claim/i)).toBeInTheDocument();
  });

  it("links to the detail page via an overlay link", () => {
    render(<ExerciseCard ex={base} />);
    expect(screen.getByRole("link", { name: "View Neck Rotation" }))
      .toHaveAttribute("href", "/exercises/neck-rotation");
  });

  it("shows direct source links when sources are present", () => {
    render(
      <ExerciseCard
        ex={{
          ...base,
          sources: [
            {
              slug: "orthoinfo-aaos",
              name: "OrthoInfo — AAOS",
              domain: "www.orthoinfo.org",
              url: "https://www.orthoinfo.org/recovery/knee-conditioning-program/",
              authority: "high",
              license: "restricted",
            },
            {
              slug: "versus-arthritis",
              name: "Versus Arthritis",
              domain: "www.arthritis-uk.org",
              url: "https://www.arthritis-uk.org/exercise",
              authority: "high",
              license: "unknown",
            },
          ],
        }}
      />,
    );
    const external = screen.getByRole("link", { name: /orthoinfo\.org/ }) as HTMLAnchorElement;
    expect(external).toHaveAttribute("href", "https://www.orthoinfo.org/recovery/knee-conditioning-program/");
    expect(external).toHaveAttribute("target", "_blank");
    expect(screen.getByRole("link", { name: /arthritis-uk\.org/ })).toBeInTheDocument();
    // card link still present and distinct
    expect(screen.getByRole("link", { name: "View Neck Rotation" })).toBeInTheDocument();
    expect(screen.getByText("Source")).toBeInTheDocument();
  });

  it("labels curated records when no external sources exist", () => {
    render(<ExerciseCard ex={base} />);
    expect(screen.getByText("Curated by Easeur editorial team")).toBeInTheDocument();
  });
});
