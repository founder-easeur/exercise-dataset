import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
import { PoseDiagram } from "@/components/pose-diagram";

describe("PoseDiagram", () => {
  it("normalizes positions to a known pose", () => {
    for (const position of ["standing", "seated", "supine", "side-lying", "on all fours", "half-kneeling", null, "weird value"]) {
      const { container, unmount } = render(
        <PoseDiagram position={position} movement="rotation" regions={["neck"]} />,
      );
      expect(container.querySelector("svg")).toBeInTheDocument();
      unmount();
    }
  });

  it("marks target regions with pulsing markers", () => {
    const { container } = render(
      <PoseDiagram position="seated" movement="flexion" regions={["neck", "shoulder"]} />,
    );
    const markers = container.querySelectorAll("circle[r='5']");
    expect(markers.length).toBe(2);
    expect(container.querySelectorAll(".pose-marker").length).toBe(2);
  });

  it("applies movement-specific animation class", () => {
    const { container: rotate } = render(
      <PoseDiagram position="standing" movement="rotation" regions={["neck"]} />,
    );
    expect(rotate.querySelector(".pose-rotate")).toBeTruthy();

    const { container: sway } = render(
      <PoseDiagram position="standing" movement="flexion" regions={["lower-back"]} />,
    );
    expect(sway.querySelector(".pose-sway")).toBeTruthy();
  });

  it("does not animate when animate=false", () => {
    const { container } = render(
      <PoseDiagram position="standing" movement="rotation" regions={["neck"]} animate={false} />,
    );
    expect(container.querySelector(".pose-rotate")).toBeFalsy();
    expect(container.querySelector(".pose-marker")).toBeFalsy();
  });
});
