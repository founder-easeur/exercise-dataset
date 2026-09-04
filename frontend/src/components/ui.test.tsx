import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  Badge, ConfidenceBar, CoverageStatusBadge, LicenseBadge, OriginBadge, ReviewStatusPill,
} from "@/components/ui";

describe("UI badges", () => {
  it("review status pill renders humanized status", () => {
    render(<ReviewStatusPill status="pending_review" />);
    expect(screen.getByText("pending review")).toBeInTheDocument();
  });

  it("origin badge distinguishes curated and aggregated", () => {
    const { rerender } = render(<OriginBadge origin="curated" />);
    expect(screen.getByText("curated")).toBeInTheDocument();
    rerender(<OriginBadge origin="aggregated" />);
    expect(screen.getByText("aggregated")).toBeInTheDocument();
  });

  it("medical badge is explicit", () => {
    render(<Badge className="">medical claim</Badge>);
    expect(screen.getByText("medical claim")).toBeInTheDocument();
  });

  it.each([
    ["excellent", "excellent"],
    ["limited", "limited"],
    ["missing", "missing"],
    ["needs_review", "needs review"],
  ] as const)("coverage status %s renders %s", (status, label) => {
    const { unmount } = render(<CoverageStatusBadge status={status} />);
    expect(screen.getByText(label)).toBeInTheDocument();
    unmount();
  });

  it.each([
    ["cc_by", "cc by"],
    ["unknown", "unknown"],
    ["restricted", "restricted"],
  ] as const)("license %s renders %s", (license, label) => {
    const { unmount } = render(<LicenseBadge license={license} />);
    expect(screen.getByText(label)).toBeInTheDocument();
    unmount();
  });
});

describe("ConfidenceBar", () => {
  it("renders percentage", () => {
    render(<ConfidenceBar value={0.92} />);
    expect(screen.getByText("92%")).toBeInTheDocument();
  });
  it("shows low-confidence value", () => {
    render(<ConfidenceBar value={0.4} />);
    expect(screen.getByText("40%")).toBeInTheDocument();
  });
});
