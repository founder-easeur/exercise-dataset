"""Curated exercises: lower back / core / breathing / recovery."""
from __future__ import annotations

TORSO_EXERCISES: list[dict] = [
    dict(slug="child-pose", name="Child's Pose",
        aliases=["balasana", "kneeling back stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="kneeling",
        regions=[("lower-back", "primary"), ("upper-back", "secondary"), ("hip", "secondary")],
        muscles=[("lumbar-erector-spinae", "stretch_target"), ("latissimus-dorsi", "stretch_target"),
                 ("gluteus-maximus", "stretch_target")],
        joints=[("lumbar-spine", "flexion")], equipment=["mat"],
        instructions=("1. Kneel and sit the hips back onto the heels.\n"
                      "2. Walk the hands forward, resting the forehead down.\n"
                      "3. Let the back round softly; breathe into the ribs.\n"
                      "4. Hold 30-60 seconds, walking hands to bias each side."),
        breathing="Deep, low ribcage breathing.",
        safety="Pad behind the knees or widen them if hips or knees complain.",
        dosage="3 x 45 seconds"),
    dict(slug="supine-spinal-twist", name="Supine Spinal Twist",
        aliases=["lying trunk rotation", "supine lumbar rotation stretch", "lying spinal twist"],
        type="stretching", movement="rotation", difficulty="beginner", position="supine",
        regions=[("lower-back", "primary"), ("chest", "secondary")],
        muscles=[("lumbar-erector-spinae", "stretch_target"), ("obliques", "stretch_target"),
                 ("gluteus-medius", "secondary"), ("piriformis", "secondary")],
        joints=[("lumbar-spine", "rotation"), ("thoracic-spine", "rotation")],
        equipment=["mat"],
        instructions=("1. Lie on your back, arms out in a T.\n"
                      "2. Draw the knees halfway up and let them fall gently to one side.\n"
                      "3. Turn the head opposite the knees; shoulders stay heavy.\n"
                      "4. Breathe 30-45 seconds and switch sides."),
        breathing="Long exhales deepen the twist safely.",
        safety="Place a cushion under the knees to reduce twist depth.",
        dosage="2 x 45 seconds per side"),
    dict(slug="lumbar-flexion-stretch", name="Single Knee-to-Chest",
        aliases=["knee to chest stretch", "double knee to chest"],
        type="stretching", movement="flexion", difficulty="beginner", position="supine",
        regions=[("lower-back", "primary"), ("hip", "secondary")],
        muscles=[("lumbar-erector-spinae", "stretch_target"), ("gluteus-maximus", "stretch_target")],
        joints=[("lumbar-spine", "flexion"), ("hip-joint", "flexion")], equipment=["mat"],
        instructions=("1. Lie on your back, legs straight.\n"
                      "2. Draw one knee toward the chest with both hands.\n"
                      "3. Keep the other leg heavy on the floor.\n"
                      "4. Hold 30 seconds; repeat 2-3 times per leg."),
        breathing="Exhale to draw the knee closer.",
        safety="Keep the tailbone on the floor; avoid lifting the head.",
        dosage="3 x 30 seconds per side"),
    dict(slug="ql-side-bend-stretch", name="Standing QL Side-Bend Stretch",
        aliases=["quadratus lumborum stretch", "standing side bend stretch"],
        type="stretching", movement="lateral flexion", difficulty="beginner", position="standing",
        regions=[("lower-back", "primary")],
        muscles=[("quadratus-lumborum", "stretch_target"), ("obliques", "stretch_target"),
                 ("latissimus-dorsi", "secondary")],
        joints=[("lumbar-spine", "lateral flexion")], equipment=[],
        instructions=("1. Stand tall, feet hip-width; reach one arm overhead.\n"
                      "2. Bend directly sideways, reaching long over the head.\n"
                      "3. Push the opposite hip gently toward the floor.\n"
                      "4. Hold 20-30 seconds, breathing into the stretched side."),
        breathing="Direct slow breaths into the ribs on the open side.",
        safety="Bend like a willow, not an arch — keep the body in one plane.",
        dosage="2-3 x 30 seconds per side"),
    dict(slug="prone-press-up", name="Prone Press-Up",
        aliases=["cobra stretch", "extension stretch prone", "mckenzie extension"],
        type="mobility", movement="extension", difficulty="beginner", position="prone",
        regions=[("lower-back", "primary"), ("chest", "secondary")],
        muscles=[("rectus-abdominis", "stretch_target"), ("obliques", "stretch_target"),
                 ("pectoralis-major", "stretch_target"), ("lumbar-erector-spinae", "primary")],
        joints=[("lumbar-spine", "extension")], equipment=["mat"],
        instructions=("1. Lie face down, hands under the shoulders.\n"
                      "2. Press the chest up, keeping the hips on the floor.\n"
                      "3. Rise only as far as comfortable; exhale at the top.\n"
                      "4. Lower slowly; repeat 10 times."),
        breathing="Exhale pressing up; inhale lowering.",
        safety="Keep the low back relaxed — arms do the pressing. Stop if symptoms travel down a leg.",
        clinical="Extension-based exercise common in mechanical low-back care (McKenzie method family).",
        contra="Avoid with suspected acute disc issues that worsen with extension or leg symptoms.",
        dosage="10 repetitions"),
    dict(slug="pelvic-tilt", name="Pelvic Tilt",
        aliases=["posterior pelvic tilt exercise", "lumbar pelvic tilt"],
        type="physiotherapy", movement="flexion", difficulty="beginner", position="supine",
        regions=[("lower-back", "primary")],
        muscles=[("transversus-abdominis", "primary"), ("rectus-abdominis", "primary"),
                 ("lumbar-erector-spinae", "stretch_target")],
        joints=[("lumbar-spine", "flexion")], equipment=["mat"],
        instructions=("1. Lie on your back, knees bent, feet flat.\n"
                      "2. Flatten the low back into the floor by tilting the pelvis back.\n"
                      "3. Feel the deep abdominals engage gently.\n"
                      "4. Hold 5 seconds, release halfway; repeat 10-15 times."),
        breathing="Exhale on the tilt.",
        safety="Subtle motion of a few degrees — no forcing.",
        clinical="Foundational motor-control drill in low-back pain rehabilitation.",
        dosage="3 x 10-15"),
    dict(slug="dead-bug", name="Dead Bug",
        aliases=["dead bug exercise", "supine alternate limb extension"],
        type="strength", movement="anti-extension", difficulty="beginner", position="supine",
        regions=[("lower-back", "primary")],
        muscles=[("transversus-abdominis", "primary"), ("rectus-abdominis", "stabilizer"),
                 ("obliques", "stabilizer"), ("diaphragm", "stabilizer")],
        joints=[("lumbar-spine", None), ("hip-joint", "flexion")], equipment=["mat"],
        instructions=("1. Lie on your back, arms vertical, knees stacked over hips at 90°.\n"
                      "2. Press the low back gently into the floor.\n"
                      "3. Lower the opposite arm and leg slowly toward the floor.\n"
                      "4. Return and alternate; the back never arches."),
        breathing="Exhale as limbs extend.",
        safety="If the back arches, shorten the lever — move legs only.",
        dosage="3 x 10 total reps"),
    dict(slug="bird-dog", name="Bird Dog",
        aliases=["quadruped alternate limb raise", "bird dog exercise"],
        type="strength", movement="anti-extension", difficulty="beginner", position="quadruped",
        regions=[("lower-back", "primary")],
        muscles=[("multifidus", "primary"), ("lumbar-erector-spinae", "primary"),
                 ("gluteus-maximus", "secondary"), ("transversus-abdominis", "stabilizer")],
        joints=[("lumbar-spine", "extension"), ("hip-joint", "extension")], equipment=["mat"],
        instructions=("1. From hands and knees, find a neutral spine.\n"
                      "2. Reach one arm forward and the opposite leg back.\n"
                      "3. Imagine balancing a wine glass on your low back.\n"
                      "4. Hold 3-5 seconds; switch sides with control."),
        breathing="Exhale reaching out.",
        safety="Move limbs without letting the pelvis tilt or rotate.",
        clinical="Core-stabilisation staple for low-back rehabilitation programmes.",
        dosage="3 x 8 per side"),
    dict(slug="glute-bridge", name="Glute Bridge",
        aliases=["bridging exercise", "supine hip bridge"],
        type="strength", movement="extension", difficulty="beginner", position="supine",
        regions=[("hip", "primary"), ("lower-back", "secondary")],
        muscles=[("gluteus-maximus", "primary"), ("biceps-femoris", "secondary"),
                 ("transversus-abdominis", "stabilizer")],
        joints=[("hip-joint", "extension")], equipment=["mat"],
        instructions=("1. Lie on your back, knees bent, feet hip-width.\n"
                      "2. Drive through the heels to lift the hips into a straight line.\n"
                      "3. Squeeze the glutes at the top for 2 seconds — ribs stay down.\n"
                      "4. Lower one vertebra at a time."),
        breathing="Exhale lifting.",
        safety="If hamstrings cramp, feet closer to hips; glutes lead, not low back.",
        dosage="3 x 12-15"),
    dict(slug="diaphragmatic-breathing", name="Diaphragmatic Breathing",
        aliases=["belly breathing", "abdominal breathing exercise"],
        type="breathing", movement=None, difficulty="beginner", position="supine",
        regions=[("lower-back", "primary"), ("whole-body", "secondary")],
        muscles=[("diaphragm", "primary"), ("obliques", "secondary"),
                 ("scalenes", "stretch_target")],
        joints=[], equipment=["mat", "pillow"],
        instructions=("1. Lie comfortably, one hand on the chest, one on the belly.\n"
                      "2. Inhale through the nose so the belly hand rises first.\n"
                      "3. Exhale slowly through pursed lips, belly falling.\n"
                      "4. Continue 3-5 minutes at an easy rhythm (about 6 breaths/minute)."),
        breathing="Nasal inhale 4s, gentle exhale 6s.",
        safety=None,
        clinical="Foundation of relaxation, COPD and chronic pain breathing retraining programmes.",
        dosage="5 minutes daily"),
    dict(slug="box-breathing", name="Box Breathing",
        aliases=["square breathing", "4-4-4-4 breathing"],
        type="breathing", movement=None, difficulty="beginner", position="seated",
        regions=[("whole-body", "primary")],
        muscles=[("diaphragm", "primary")],
        joints=[], equipment=[],
        instructions=("1. Inhale through the nose for 4 counts.\n"
                      "2. Hold gently for 4 counts.\n"
                      "3. Exhale smoothly for 4 counts.\n"
                      "4. Hold empty for 4; repeat the square 8-10 rounds."),
        breathing="Even, quiet, nose-led.",
        safety="If light-headed, drop the holds; keep counts shorter.",
        dosage="8-10 rounds"),
    dict(slug="pelvic-floor-activation", name="Pelvic Floor Activation",
        aliases=["kegel exercise", "pelvic floor exercise"],
        type="physiotherapy", movement=None, difficulty="beginner", position="supine",
        regions=[("lower-back", "primary")],
        muscles=[("pelvic-floor", "primary"), ("transversus-abdominis", "stabilizer"),
                 ("diaphragm", "stabilizer")],
        joints=[], equipment=["mat"],
        instructions=("1. Lie with knees bent; breathe normally.\n"
                      "2. Gently draw the pelvic floor up and in, as if stopping the flow of urine.\n"
                      "3. Hold 3-5 seconds at 30-50% effort, fully releasing between.\n"
                      "4. Coordinate with an exhale; repeat 10 times."),
        breathing="Exhale during the lift.",
        safety="Full relaxation between contractions matters as much as the lift.",
        clinical="Core component of pelvic-health physiotherapy programmes.",
        dosage="10 x 5-second holds"),
    dict(slug="seated-trunk-rotation", name="Seated Trunk Rotation",
        aliases=["seated spinal twist", "chair trunk rotation"],
        type="mobility", movement="rotation", difficulty="beginner", position="seated",
        regions=[("lower-back", "primary"), ("upper-back", "primary")],
        muscles=[("obliques", "stretch_target"), ("thoracic-erector-spinae", "stretch_target"),
                 ("quadratus-lumborum", "secondary")],
        joints=[("thoracic-spine", "rotation"), ("lumbar-spine", "rotation")],
        equipment=["chair"],
        instructions=("1. Sit tall on a chair, feet flat.\n"
                      "2. Hold the seat back with both hands on one side.\n"
                      "3. Rotate the chest around a tall spine, sitting bones even.\n"
                      "4. Hold 20 seconds; repeat twice per side."),
        breathing="Inhale to lengthen; exhale to rotate further.",
        safety="Rotate the ribcage, not just the shoulders or neck.",
        dosage="2 x 20 seconds per side"),
    dict(slug="cat-cow-seated", name="Seated Cat-Cow",
        aliases=["chair cat cow", "seated spinal flexion extension"],
        type="mobility", movement="flexion", difficulty="beginner", position="seated",
        regions=[("lower-back", "primary"), ("upper-back", "primary")],
        muscles=[("lumbar-erector-spinae", "stretch_target"), ("rectus-abdominis", "primary"),
                 ("thoracic-erector-spinae", "stretch_target")],
        joints=[("lumbar-spine", "flexion"), ("thoracic-spine", "extension")],
        equipment=["chair"],
        instructions=("1. Sit with hands on knees, feet flat.\n"
                      "2. Exhale: round back, tuck chin and tailbone.\n"
                      "3. Inhale: lift chest and tailbone, gaze slightly up.\n"
                      "4. Flow 10 slow cycles."),
        breathing="Exhale to round, inhale to arch.",
        safety=None,
        dosage="10 cycles"),
]
