/**
 * Animated SVG movement preview, rendered from structured exercise data
 * (position, movement pattern, target regions). Deterministic, dependency-free
 * and licensed-clean — it is code, not media. Works alongside the static
 * illustrations from the media registry.
 */

type Joint = [number, number];
interface Pose {
  joints: Record<string, Joint>;
  chair?: boolean;
  floor?: boolean;
}

const POSES: Record<string, Pose> = {
  standing: {
    joints: { head: [100, 30], neck: [100, 46], shoulder: [100, 56], elbow: [112, 84], wrist: [120, 110], hip: [100, 100], knee: [102, 128], ankle: [104, 150] },
  },
  seated: {
    joints: { head: [100, 30], neck: [100, 46], shoulder: [100, 56], elbow: [114, 84], wrist: [122, 108], hip: [100, 102], knee: [134, 108], ankle: [138, 138] },
    chair: true,
  },
  seated_floor: {
    joints: { head: [100, 34], neck: [100, 50], shoulder: [100, 60], elbow: [114, 88], wrist: [120, 112], hip: [100, 106], knee: [132, 112], ankle: [110, 130] },
    floor: true,
  },
  supine: {
    joints: { head: [34, 102], neck: [52, 100], shoulder: [64, 98], elbow: [94, 108], wrist: [122, 98], hip: [104, 100], knee: [140, 84], ankle: [168, 98] },
    floor: true,
  },
  prone: {
    joints: { head: [168, 98], neck: [150, 100], shoulder: [138, 102], elbow: [108, 92], wrist: [82, 102], hip: [98, 104], knee: [64, 96], ankle: [34, 106] },
    floor: true,
  },
  side_lying: {
    joints: { head: [34, 98], neck: [52, 98], shoulder: [64, 100], elbow: [92, 112], wrist: [114, 102], hip: [102, 102], knee: [134, 84], ankle: [160, 102] },
    floor: true,
  },
  quadruped: {
    joints: { head: [162, 66], neck: [150, 76], shoulder: [134, 86], elbow: [140, 114], wrist: [146, 140], hip: [86, 88], knee: [78, 116], ankle: [84, 140] },
  },
  kneeling: {
    joints: { head: [96, 30], neck: [96, 46], shoulder: [96, 56], elbow: [110, 84], wrist: [118, 110], hip: [96, 102], knee: [128, 124], ankle: [130, 148], kneeBack: [72, 138], ankleBack: [48, 142] },
    floor: true,
  },
};

function normalizePosition(raw?: string | null): keyof typeof POSES {
  const p = (raw || "").toLowerCase();
  if (p.includes("quadruped") || p.includes("all four")) return "quadruped";
  if (p.includes("side-lying") || p.includes("side lying")) return "side_lying";
  if (p.includes("half-kneel")) return "kneeling";
  if (p.includes("kneel")) return "kneeling";
  if (p.includes("prone")) return "prone";
  if (p.includes("supine") || p.includes("on back")) return "supine";
  if (p.includes("floor") || p.includes("cross")) return "seated_floor";
  if (p.includes("seat") || p.includes("sit")) return "seated";
  return "standing";
}

/** Movement keyword → animation class applied to the moving body part. */
function animationClass(movement?: string | null): string {
  const m = (movement || "").toLowerCase();
  if (m.includes("rotat") || m.includes("circumduct")) return "pose-rotate";
  if (m.includes("flex") || m.includes("exten") || m.includes("dorsi")) return "pose-sway";
  if (m.includes("abduct") || m.includes("adduct") || m.includes("retract")) return "pose-swing";
  return "pose-pulse";
}

/** Which body-part group animates, and its transform origin joint. */
const MOVING_PART: Record<string, { group: "head" | "torso" | "arm" | "leg"; origin: string }> = {
  neck: { group: "head", origin: "neck" },
  jaw: { group: "head", origin: "neck" },
  shoulder: { group: "arm", origin: "shoulder" },
  chest: { group: "arm", origin: "shoulder" },
  "upper-back": { group: "arm", origin: "shoulder" },
  elbow: { group: "arm", origin: "elbow" },
  forearm: { group: "arm", origin: "elbow" },
  wrist: { group: "arm", origin: "wrist" },
  hand: { group: "arm", origin: "wrist" },
  "lower-back": { group: "torso", origin: "hip" },
  hip: { group: "leg", origin: "hip" },
  knee: { group: "leg", origin: "knee" },
  calf: { group: "leg", origin: "knee" },
  ankle: { group: "leg", origin: "ankle" },
  foot: { group: "leg", origin: "ankle" },
  "whole-body": { group: "torso", origin: "hip" },
};

/** Region slug → anchor point (joint name or midpoint helper). */
function regionAnchor(region: string, j: Record<string, Joint>): Joint | null {
  const mid = (a: string, b: string, t = 0.5): Joint => [
    j[a][0] + (j[b][0] - j[a][0]) * t,
    j[a][1] + (j[b][1] - j[a][1]) * t,
  ];
  const map: Record<string, Joint | null> = {
    neck: j.neck, jaw: j.head, shoulder: j.shoulder, elbow: j.elbow,
    wrist: j.wrist, hand: j.wrist, hip: j.hip, knee: j.knee, ankle: j.ankle,
    foot: j.ankle, forearm: mid("elbow", "wrist"), calf: mid("knee", "ankle"),
    chest: mid("shoulder", "hip", 0.33), "upper-back": mid("shoulder", "hip", 0.33),
    "lower-back": mid("shoulder", "hip", 0.7), "whole-body": mid("shoulder", "hip", 0.5),
  };
  return map[region] || null;
}

export function PoseDiagram({
  position, movement, regions, size = 300, animate = true,
}: {
  position?: string | null;
  movement?: string | null;
  regions: string[];
  size?: number;
  animate?: boolean;
}) {
  const poseKey = normalizePosition(position);
  const pose = POSES[poseKey];
  const j = pose.joints;
  const anim = animate ? animationClass(movement) : "";
  const primary = regions.find((r) => MOVING_PART[r]) || regions[0] || "whole-body";
  const part = MOVING_PART[primary] || MOVING_PART["whole-body"];
  const origin = j[part.origin] || j.hip;

  const line = (a: Joint, b: Joint, width = 5) => (
    <line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke="currentColor" strokeWidth={width} strokeLinecap="round" />
  );
  const groupClass = (group: string) => (part.group === group ? anim : "");
  const groupStyle = (group: string, originJoint: string): React.CSSProperties =>
    part.group === group ? { transformOrigin: `${j[originJoint][0]}px ${j[originJoint][1]}px` } : {};

  return (
    <svg viewBox="0 0 200 164" width={size} className="mx-auto max-w-full text-slate-400 dark:text-slate-500" role="img"
      aria-label={`Movement preview: ${poseKey.replace(/_/g, " ")} position, ${movement || "gentle"} movement`}>
      {/* floor / chair */}
      {pose.floor ? <line x1="16" y1="152" x2="184" y2="152" stroke="currentColor" strokeWidth="2" opacity="0.35" /> : null}
      {pose.chair ? (
        <g opacity="0.35">
          <line x1="86" y1="104" x2="150" y2="104" strokeWidth="3" />
          <line x1="86" y1="60" x2="86" y2="104" strokeWidth="3" />
          <line x1="92" y1="104" x2="92" y2="150" strokeWidth="3" />
          <line x1="144" y1="104" x2="144" y2="150" strokeWidth="3" />
        </g>
      ) : null}

      {/* far-side limbs (context) */}
      <g opacity="0.4">
        {line([j.shoulder[0] - 4, j.shoulder[1]], [j.elbow[0] - 6, j.elbow[1]], 4)}
        {line([j.elbow[0] - 6, j.elbow[1]], [j.wrist[0] - 6, j.wrist[1]], 4)}
        {line([j.hip[0] - 4, j.hip[1]], [j.knee[0] - 4, j.knee[1]], 5)}
        {line([j.knee[0] - 4, j.knee[1]], [j.ankle[0] - 4, j.ankle[1]], 4)}
      </g>

      {/* leg */}
      <g className={groupClass("leg")} style={groupStyle("leg", part.group === "leg" ? part.origin : "hip")}>
        {line(j.hip, j.knee)}
        {line(j.knee, j.ankle, 4)}
        {"kneeBack" in j ? (
          <>
            {line(j.hip, j.kneeBack)}
            {line(j.kneeBack, j.ankleBack, 4)}
          </>
        ) : null}
      </g>

      {/* torso */}
      <g className={groupClass("torso")} style={groupStyle("torso", "hip")}>
        {line(j.neck, j.hip, 9)}
      </g>

      {/* arm */}
      <g className={groupClass("arm")} style={groupStyle("arm", part.group === "arm" ? part.origin : "shoulder")}>
        {line(j.shoulder, j.elbow)}
        {line(j.elbow, j.wrist, 4)}
      </g>

      {/* head */}
      <g className={groupClass("head")} style={groupStyle("head", "neck")}>
        <circle cx={j.head[0]} cy={j.head[1]} r="13" fill="currentColor" />
      </g>

      {/* target-region markers */}
      {regions.slice(0, 3).map((r) => {
        const a = regionAnchor(r, j);
        if (!a) return null;
        return (
          <g key={r}>
            <circle cx={a[0]} cy={a[1]} r="14" fill="#6366f1" opacity="0.25" className={animate ? "pose-marker" : ""} />
            <circle cx={a[0]} cy={a[1]} r="5" fill="#6366f1" />
          </g>
        );
      })}
    </svg>
  );
}
