"""Curated exercises: hip / pelvis and knee."""
from __future__ import annotations

HIP_KNEE_EXERCISES: list[dict] = [
    # ------------------------------------------------------------------ hip
    dict(slug="seated-figure-4-stretch", name="Seated Figure-4 Stretch",
        aliases=["seated piriformis stretch", "figure four stretch", "piriformis stretch seated"],
        type="stretching", movement="external rotation", difficulty="beginner", position="seated",
        regions=[("hip", "primary")],
        muscles=[("piriformis", "stretch_target"), ("obturator-internus", "stretch_target"),
                 ("superior-gemellus", "stretch_target"), ("gluteus-maximus", "secondary")],
        joints=[("hip-joint", "internal rotation"), ("sacroiliac-joint", None)], equipment=["chair"],
        instructions=("1. Sit tall and cross one ankle over the opposite knee, making a figure 4.\n"
                      "2. Keep the crossed knee open (falling outward).\n"
                      "3. Hinge forward from the hips with a tall spine until a stretch appears in the buttock.\n"
                      "4. Hold 30 seconds; switch sides."),
        breathing="Exhale as you hinge forward.",
        safety="Stretch the buttock, not the knee: never press down on the crossed knee.",
        clinical="Piriformis and deep rotator stretch common in sciatica-adjacent programmes.",
        dosage="3 x 30 seconds per side"),
    dict(slug="pigeon-pose", name="Pigeon Pose",
        aliases=["pigeon stretch", "eka pada rajakapotasana"],
        type="stretching", movement="external rotation", difficulty="intermediate", position="kneeling",
        regions=[("hip", "primary")],
        muscles=[("piriformis", "stretch_target"), ("gluteus-maximus", "stretch_target"),
                 ("obturator-externus", "stretch_target"), ("quadratus-femoris", "stretch_target"),
                 ("iliopsoas" if False else "pectineus", "secondary")],
        joints=[("hip-joint", "external rotation")], equipment=["mat", "pillow"],
        instructions=("1. From all fours, bring one knee forward and lay it diagonally under the chest.\n"
                      "2. Slide the other leg long behind, toes untucked.\n"
                      "3. Level the hips (a pillow under the buttock helps) and settle.\n"
                      "4. Stay upright or fold forward onto the forearms for 30-60 seconds."),
        breathing="Slow breathing releases the hip on every exhale.",
        safety="Knee discomfort means back off: do the figure-4 version instead.",
        contra="Careful with known hip impingement or knee injuries.",
        dosage="1-2 x 45 seconds per side"),
    dict(slug="kneeling-hip-flexor-stretch", name="Kneeling Hip Flexor Stretch",
        aliases=["runner's lunge stretch", "low lunge stretch", "hip flexor stretch kneeling"],
        type="stretching", movement="extension", difficulty="beginner", position="half-kneeling",
        regions=[("hip", "primary")],
        muscles=[("iliopsoas", "stretch_target"), ("rectus-femoris", "stretch_target"),
                 ("pectineus", "secondary"), ("tensor-fasciae-latae", "secondary")],
        joints=[("hip-joint", "extension")], equipment=["mat", "pillow"],
        instructions=("1. Kneel on one knee (cushion under it), the other foot forward.\n"
                      "2. Tuck the tailbone to posteriorly tilt the pelvis — this is the stretch.\n"
                      "3. Squeeze the back-leg glute and gently shift forward a few centimetres.\n"
                      "4. Hold 30 seconds, ribs stacked over the pelvis."),
        breathing="Exhale to tuck; breathe into the front of the hip.",
        safety="The pelvis tuck comes first; without it the low back takes the stretch.",
        clinical="Key exercise for shortened hip flexors in sedentary and postpartum populations.",
        dosage="2-3 x 30 seconds per side"),
    dict(slug="couch-stretch", name="Couch Stretch",
        aliases=["wall quad stretch", "deep hip flexor and quad stretch"],
        type="stretching", movement="extension", difficulty="advanced", position="half-kneeling",
        regions=[("hip", "primary"), ("knee", "secondary")],
        muscles=[("iliopsoas", "stretch_target"), ("rectus-femoris", "stretch_target"),
                 ("vastus-lateralis", "stretch_target")],
        joints=[("hip-joint", "extension"), ("knee-joint", "flexion")], equipment=["wall", "mat", "pillow"],
        instructions=("1. Face away from a wall/couch, back knee on a cushion, shin up the wall.\n"
                      "2. Squeeze the back glute to tuck the pelvis before anything else.\n"
                      "3. Bring the torso upright in stages — hands to floor, then tall.\n"
                      "4. Breathe 45+ seconds; intensity should be strong but tolerable."),
        breathing="Slow, deliberate breathing; do not brace.",
        safety="Progress slowly over weeks; knee pain means raise the foot higher or reduce knee bend.",
        contra="Skip with anterior knee pain or recent patellar injury.",
        dosage="1-2 x 45 seconds per side"),
    dict(slug="butterfly-stretch", name="Butterfly Stretch",
        aliases=["baddha konasana", "seated groin stretch", "adductor stretch seated"],
        type="stretching", movement="adduction", difficulty="beginner", position="seated on floor",
        regions=[("hip", "primary")],
        muscles=[("adductor-longus", "stretch_target"), ("adductor-magnus", "stretch_target"),
                 ("gracilis", "stretch_target"), ("piriformis", "secondary")],
        joints=[("hip-joint", "abduction")], equipment=["mat"],
        instructions=("1. Sit with the soles of the feet together, knees out.\n"
                      "2. Hold the ankles, sit tall.\n"
                      "3. Hinge forward from the hips, leading with the chest.\n"
                      "4. Hold 30-60 seconds; knees float — no pressing."),
        breathing="Long exhales; imagine the knees floating up on inhales.",
        safety="Never bounce or push knees down; gravity and time do the work.",
        dosage="2-3 x 45 seconds"),
    dict(slug="ninety-ninety-stretch", name="90/90 Hip Stretch",
        aliases=["90 90 stretch", "hip rotator stretch 90/90"],
        type="mobility", movement="rotation", difficulty="intermediate", position="seated on floor",
        regions=[("hip", "primary")],
        muscles=[("piriformis", "stretch_target"), ("obturator-internus", "stretch_target"),
                 ("gluteus-maximus", "stretch_target"), ("iliopsoas", "stretch_target"),
                 ("tensor-fasciae-latae", "secondary")],
        joints=[("hip-joint", "internal rotation"), ("hip-joint", "external rotation")],
        equipment=["mat"],
        instructions=("1. Sit with the front leg bent 90° in front and the back leg bent 90° to the side.\n"
                      "2. Sit tall, hands lightly behind for balance.\n"
                      "3. Lead the chest over the front shin for external-rotation bias.\n"
                      "4. Switch legs by rotating the knees together through the middle."),
        breathing="Exhale into each position; 30-45 seconds each side.",
        safety="Pad under the back knee; keep the sit bones heavy.",
        dosage="2 rounds per side"),
    dict(slug="standing-hip-flexor-stretch", name="Standing Hip Flexor Stretch",
        aliases=["standing lunge stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("iliopsoas", "stretch_target"), ("rectus-femoris", "stretch_target")],
        joints=[("hip-joint", "extension")], equipment=[],
        instructions=("1. Take a long step back with one leg, both feet pointing forward.\n"
                      "2. Tuck the tailbone, squeeze the back glute.\n"
                      "3. Shift forward until the front of the back hip lengthens.\n"
                      "4. Hold 30 seconds per side."),
        breathing="Exhale to deepen.",
        safety="Keep the back knee soft; ribs down.",
        dosage="2 x 30 seconds per side"),
    dict(slug="glute-bridge-march", name="Glute Bridge March",
        aliases=["marching bridge", "single leg bridge progression"],
        type="strength", movement="anti-extension", difficulty="intermediate", position="supine",
        regions=[("hip", "primary"), ("lower-back", "secondary")],
        muscles=[("gluteus-maximus", "primary"), ("gluteus-medius", "stabilizer"),
                 ("transversus-abdominis", "stabilizer")],
        joints=[("hip-joint", "extension")], equipment=["mat"],
        instructions=("1. Lift into a glute bridge and hold the line.\n"
                      "2. Lift one knee a few centimetres toward the chest without dropping a hip.\n"
                      "3. Place it down and lift the other — marching.\n"
                      "4. Keep the hips level like headlights."),
        breathing="Exhale on each knee lift.",
        safety="If hips wobble, lower and re-bridge; quality first.",
        dosage="3 x 10 marches"),
    dict(slug="side-lying-hip-abduction", name="Side-Lying Hip Abduction",
        aliases=["side leg raises", "clamshell progression abduction"],
        type="physiotherapy", movement="abduction", difficulty="beginner", position="side-lying",
        regions=[("hip", "primary")],
        muscles=[("gluteus-medius", "primary"), ("gluteus-minimus", "primary"),
                 ("tensor-fasciae-latae", "secondary")],
        joints=[("hip-joint", "abduction")], equipment=["mat"],
        instructions=("1. Lie on your side, body straight, slight forward lean.\n"
                      "2. Lift the top leg 30-45°, heel slightly behind the line of the body.\n"
                      "3. Toes point forward — lead with the heel.\n"
                      "4. Lower slowly; feel the side-of-hip muscle work."),
        breathing="Exhale lifting.",
        safety="Small range with control beats big kicks with momentum.",
        clinical="Gluteus medius strengthening for hip and knee rehabilitation, pelvic drop (Trendelenburg).",
        dosage="3 x 12-15 per side"),
    dict(slug="clamshell", name="Clamshell",
        aliases=["side-lying clam exercise", "clam shell exercise"],
        type="physiotherapy", movement="external rotation", difficulty="beginner", position="side-lying",
        regions=[("hip", "primary")],
        muscles=[("gluteus-medius", "primary"), ("gluteus-maximus", "primary"),
                 ("piriformis", "secondary")],
        joints=[("hip-joint", "external rotation")], equipment=["mat", "resistance-band"],
        instructions=("1. Lie on your side, knees bent ~45°, heels together, hips stacked.\n"
                      "2. Keeping the feet touching, rotate the top knee open like a clam.\n"
                      "3. Feel the glute behind the hip bone — not the front.\n"
                      "4. Close slowly; repeat."),
        breathing="Exhale opening.",
        safety="If you feel it at the front of the hip, roll the toes slightly down.",
        clinical="Classic gluteal activation drill; often early in hip/knee rehab programmes.",
        dosage="3 x 15 per side"),
    dict(slug="standing-hip-drop", name="Standing Hip Drop (Wall Support)",
        aliases=["hip hitch", "pelvic drop exercise"],
        type="strength", movement="elevation", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("gluteus-medius", "primary"), ("gluteus-minimus", "primary"),
                 ("quadratus-lumborum", "stabilizer")],
        joints=[("hip-joint", "elevation"), ("sacroiliac-joint", None)], equipment=["wall"],
        instructions=("1. Stand side-on to a wall, one hand on it, feet together.\n"
                      "2. Keep both knees straight and drop the inner hip toward the floor.\n"
                      "3. Then hitch it up above level, shortening the waist.\n"
                      "4. Move smoothly through drops and hitches."),
        breathing="Relaxed.",
        safety="Small motion; the standing hip does the work.",
        dosage="2 x 10 per side"),
    dict(slug="hip-circles", name="Hip Circles",
        aliases=["dynamic hip circles", "hip circumduction standing"],
        type="warmup", movement="circumduction", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("gluteus-maximus", "primary"), ("gluteus-medius", "primary"),
                 ("adductor-longus", "secondary"), ("iliopsoas", "secondary")],
        joints=[("hip-joint", "circumduction")], equipment=[],
        instructions=("1. Stand on one leg with light support at a wall.\n"
                      "2. Swing the free leg in slow, large circles.\n"
                      "3. 8 circles each direction, keeping the torso still.\n"
                      "4. Switch legs."),
        breathing="Rhythmic breathing.",
        safety="Circles grow gradually; support as needed for balance.",
        dosage="8 circles each direction per leg"),
    dict(slug="leg-swings", name="Leg Swings",
        aliases=["dynamic hamstring stretch standing", "front-to-back leg swings"],
        type="warmup", movement="flexion", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("biceps-femoris", "stretch_target"),
                 ("iliopsoas", "secondary"), ("gluteus-maximus", "stretch_target")],
        joints=[("hip-joint", "flexion"), ("hip-joint", "extension")], equipment=["wall"],
        instructions=("1. Stand side-on to a wall, one hand on it.\n"
                      "2. Swing the inside leg forward and back like a pendulum.\n"
                      "3. Start small, grow the arc gradually — 15-20 swings.\n"
                      "4. Turn around and swing the other leg."),
        breathing="Easy and continuous.",
        safety="Keep the swing relaxed; no forcing at the end range.",
        dosage="15-20 swings per leg"),
    dict(slug="itb-foam-roll", name="ITB Foam Roll",
        aliases=["iliotibial band foam rolling", "TFL foam roll", "outer thigh foam roll"],
        type="release", movement=None, difficulty="intermediate", position="side plank supported",
        regions=[("hip", "primary"), ("calf", "secondary")],
        muscles=[("iliotibial-band", "stretch_target"), ("tensor-fasciae-latae", "stretch_target"),
                 ("vastus-lateralis", "secondary")],
        joints=[], equipment=["foam-roller"],
        instructions=("1. Lie side-on with the roller under the outer thigh, other leg in front for support.\n"
                      "2. Roll slowly from just below the hip to just above the knee.\n"
                      "3. Pause 20-30 seconds on tender spots.\n"
                      "4. Keep the discomfort at 'uncomfortable but bearable' — never sharp."),
        breathing="Slow breathing softens the tissue.",
        safety="Never roll over bony prominences; the ITB itself cannot be 'stretched' — work the attached muscles.",
        clinical="Self-myofascial release used around ITB friction syndrome and runner's knee care.",
        dosage="1-2 minutes per side"),
    dict(slug="standing-adductor-stretch", name="Standing Adductor Stretch",
        aliases=["standing groin stretch", "wide leg forward fold standing"],
        type="stretching", movement="abduction", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("adductor-longus", "stretch_target"), ("adductor-magnus", "stretch_target"),
                 ("gracilis", "stretch_target")],
        joints=[("hip-joint", "abduction")], equipment=[],
        instructions=("1. Take a wide stance, toes slightly out.\n"
                      "2. Shift the hips sideways, bending one knee over its foot.\n"
                      "3. Feel the inner thigh of the straight leg lengthen.\n"
                      "4. Hold 20-30 seconds each side."),
        breathing="Exhale into the shift.",
        safety="Keep the bent knee tracking over the middle toes.",
        dosage="2 x 30 seconds per side"),
    dict(slug="sciatic-nerve-glide-supine", name="Sciatic Nerve Glide (Supine)",
        aliases=["sciatic nerve flossing", "hamstring nerve glide"],
        type="rehabilitation", movement="flexion", difficulty="intermediate", position="supine",
        regions=[("hip", "primary"), ("calf", "secondary")],
        muscles=[("sciatic-nerve", "stretch_target"), ("biceps-femoris", "secondary")],
        joints=[("hip-joint", "flexion"), ("knee-joint", "extension")], equipment=["mat", "strap"],
        instructions=("1. Lie on your back with a strap around one foot.\n"
                      "2. Straighten the knee to a comfortable tension, then flex the ankle (nerve tension).\n"
                      "3. Bend the knee again while keeping the leg up (nerve slack) — alternate like flossing.\n"
                      "4. 10-12 cycles, always below symptom threshold."),
        breathing="Slow and steady.",
        safety="Never stretch into tingling or shooting sensations — glide lightly.",
        contra="Not for acute severe nerve pain; consult a clinician first.",
        clinical="Neural mobilisation for sciatic-nerve-sensitive presentations.",
        dosage="10-12 gentle cycles per leg"),
    dict(slug="seated-hip-internal-rotation", name="Seated Hip Internal Rotation Mobility",
        aliases=["hip internal rotation exercise seated"],
        type="mobility", movement="internal rotation", difficulty="beginner", position="seated",
        regions=[("hip", "primary")],
        muscles=[("piriformis", "stretch_target"), ("obturator-internus", "stretch_target"),
                 ("gluteus-maximus", "stretch_target")],
        joints=[("hip-joint", "internal rotation")], equipment=["chair"],
        instructions=("1. Sit tall; bring one ankle to rest just above the opposite knee.\n"
                      "2. Hold the knee and shin, and gently rotate the hip inward by drawing the knee toward the midline.\n"
                      "3. Keep the sit bones even; move with breath.\n"
                      "4. 10 slow rotations per hip."),
        breathing="Exhale on rotation.",
        safety="Small arc, no knee pressure.",
        dosage="10 per side"),
    dict(slug="squat-hold", name="Deep Squat Hold",
        aliases=["resting squat", "malasana"],
        type="mobility", movement="flexion", difficulty="intermediate", position="standing",
        regions=[("hip", "primary"), ("ankle", "secondary"), ("knee", "secondary")],
        muscles=[("gluteus-maximus", "stretch_target"), ("adductor-magnus", "stretch_target"),
                 ("gastrocnemius", "stretch_target"), ("soleus", "stretch_target")],
        joints=[("hip-joint", "flexion"), ("knee-joint", "flexion"), ("ankle-joint", "dorsiflexion")],
        equipment=[],
        instructions=("1. Stand with feet shoulder-width, toes slightly out.\n"
                      "2. Descend into the deepest comfortable squat, heels down.\n"
                      "3. Use elbows to gently press knees out; chest tall.\n"
                      "4. Hold 20-60 seconds, rocking gently side to side."),
        breathing="Slow, easy breathing in the bottom.",
        safety="Heels lift? Support them on a book; knees track over toes.",
        dosage="2-3 x 30-60 seconds"),
    dict(slug="sacroiliac-stretch-side-lying", name="Side-Lying SI Joint Stretch",
        aliases=["SI joint stretch", "sacroiliac stretch"],
        type="stretching", movement="rotation", difficulty="beginner", position="side-lying",
        regions=[("hip", "primary"), ("lower-back", "secondary")],
        muscles=[("quadratus-lumborum", "stretch_target"), ("gluteus-medius", "stretch_target"),
                 ("piriformis", "secondary")],
        joints=[("sacroiliac-joint", None), ("lumbar-spine", "rotation")], equipment=["mat"],
        instructions=("1. Lie on your side at the edge of a bed, top knee dropped over the edge in front.\n"
                      "2. Let the top shoulder rotate back toward the ceiling.\n"
                      "3. Breathe into the back of the pelvis for 30 seconds.\n"
                      "4. Repeat on the other side."),
        breathing="Slow nasal breathing.",
        safety="Support the dropped knee with a cushion.",
        dosage="2 x 30 seconds per side"),
    # ----------------------------------------------------------------- knee
    dict(slug="standing-quad-stretch", name="Standing Quadriceps Stretch",
        aliases=["standing quad stretch", "flamingo stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="standing",
        regions=[("knee", "primary"), ("hip", "secondary")],
        muscles=[("rectus-femoris", "stretch_target"), ("vastus-lateralis", "stretch_target"),
                 ("vastus-medialis", "stretch_target"), ("vastus-intermedius", "stretch_target")],
        joints=[("knee-joint", "flexion"), ("hip-joint", "extension")], equipment=["wall"],
        instructions=("1. Stand on one leg (wall for balance), holding the other ankle behind you.\n"
                      "2. Keep knees together and tuck the tailbone.\n"
                      "3. Draw the knee slightly back only if the front hip needs more.\n"
                      "4. Hold 30 seconds per side."),
        breathing="Steady; relax the shoulders.",
        safety="No twisting at the knee; if it tweaks the knee, use the side-lying version.",
        dosage="2-3 x 30 seconds per side"),
    dict(slug="side-lying-quad-stretch", name="Side-Lying Quadriceps Stretch",
        aliases=["side lying quad stretch", "side-lying knee flexion stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="side-lying",
        regions=[("knee", "primary")],
        muscles=[("rectus-femoris", "stretch_target"), ("vastus-lateralis", "stretch_target"),
                 ("vastus-intermedius", "stretch_target")],
        joints=[("knee-joint", "flexion")], equipment=["mat"],
        instructions=("1. Lie on your side, bottom arm supporting the head.\n"
                      "2. Bend the top knee and hold the ankle behind you.\n"
                      "3. Keep the thigh in line with the body; tailbone tucked.\n"
                      "4. Hold 30 seconds and rotate legs."),
        breathing="Relaxed.",
        safety="Knee-friendly alternative when standing version pinches.",
        dosage="2 x 30 seconds per side"),
    dict(slug="supine-hamstring-stretch", name="Supine Hamstring Stretch With Strap",
        aliases=["lying hamstring stretch", "towel hamstring stretch", "strap hamstring stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="supine",
        regions=[("hip", "primary"), ("knee", "secondary")],
        muscles=[("biceps-femoris", "stretch_target"), ("semitendinosus", "stretch_target"),
                 ("semimembranosus", "stretch_target")],
        joints=[("hip-joint", "flexion"), ("knee-joint", "extension")], equipment=["mat", "strap"],
        instructions=("1. Lie on your back and loop a strap under one foot.\n"
                      "2. Raise the leg, knee nearly straight, to a clear hamstring stretch.\n"
                      "3. Keep the other leg heavy on the floor.\n"
                      "4. Hold 30 seconds; the knee can stay softly bent."),
        breathing="Exhale to invite the leg higher.",
        safety="Stretch the back of the thigh, not behind the knee — never yank.",
        dosage="2-3 x 30 seconds per side"),
    dict(slug="seated-hamstring-stretch", name="Seated Hamstring Stretch",
        aliases=["seated forward fold", "modified seated hamstring stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="seated on floor",
        regions=[("hip", "primary"), ("knee", "secondary")],
        muscles=[("biceps-femoris", "stretch_target"), ("semitendinosus", "stretch_target"),
                 ("semimembranosus", "stretch_target"), ("lumbar-erector-spinae", "secondary")],
        joints=[("hip-joint", "flexion")], equipment=["mat", "chair"],
        instructions=("1. Sit with one leg extended, the other bent with foot to inner thigh.\n"
                      "2. Hinge forward from the hips, chest leading.\n"
                      "3. Rest hands on the floor, a chair seat, or the shin.\n"
                      "4. Hold 30 seconds per side."),
        breathing="Long exhales fold you forward.",
        safety="A flat-back fold halfway down beats a rounded reach to the toes.",
        dosage="2 x 30 seconds per side"),
    dict(slug="short-arc-quad", name="Short-Arc Quadriceps Exercise",
        aliases=["short arc quad extension", "VMO short arc", "mini squat quad set"],
        type="physiotherapy", movement="extension", difficulty="beginner", position="supine",
        regions=[("knee", "primary")],
        muscles=[("vastus-medialis", "primary"), ("rectus-femoris", "primary"),
                 ("vastus-lateralis", "secondary")],
        joints=[("knee-joint", "extension"), ("patellofemoral-joint", "extension")],
        equipment=["mat", "pillow", "dumbbell"],
        instructions=("1. Lie on your back with a rolled towel (~15 cm) under one knee.\n"
                      "2. Straighten that knee, sliding the foot along the floor and lifting the heel.\n"
                      "3. Squeeze the thigh hard at the top for 3 seconds.\n"
                      "4. Lower slowly; repeat."),
        breathing="Exhale straightening.",
        safety="Keep the low back relaxed; only the knee works.",
        clinical="Early quadriceps re-education after knee surgery/injury; targets VMO recruitment.",
        dosage="3 x 12-15"),
    dict(slug="straight-leg-raise", name="Straight Leg Raise",
        aliases=["SLR exercise", "supine straight leg raise"],
        type="physiotherapy", movement="flexion", difficulty="beginner", position="supine",
        regions=[("hip", "primary"), ("knee", "secondary")],
        muscles=[("rectus-femoris", "primary"), ("iliopsoas", "primary"),
                 ("vastus-medialis", "stabilizer")],
        joints=[("hip-joint", "flexion")], equipment=["mat"],
        instructions=("1. Sit long, one knee bent; straighten the other leg, quad squeezed.\n"
                      "2. Lift the straight leg to the height of the bent knee.\n"
                      "3. Hold 2-3 seconds; lower with control.\n"
                      "4. Keep the pelvis still."),
        breathing="Exhale lifting.",
        safety="If the hip front grips, reduce height; quality over height.",
        clinical="Foundational quadriceps/hip-flexor exercise post knee surgery.",
        dosage="3 x 12 per leg"),
    dict(slug="terminal-knee-extension", name="Terminal Knee Extension (Band)",
        aliases=["TKE band exercise", "terminal knee extension resistance band"],
        type="rehabilitation", movement="extension", difficulty="beginner", position="standing",
        regions=[("knee", "primary")],
        muscles=[("vastus-medialis", "primary"), ("vastus-lateralis", "primary"),
                 ("popliteus", "stabilizer")],
        joints=[("knee-joint", "extension"), ("patellofemoral-joint", "extension")],
        equipment=["resistance-band"],
        instructions=("1. Loop a band behind the knee, anchored at knee height.\n"
                      "2. Start with the exercised knee slightly bent, weight on that leg.\n"
                      "3. Straighten the knee fully against the band, squeezing the quad.\n"
                      "4. Return slowly to the slight bend; repeat."),
        breathing="Exhale on extension.",
        safety="Light band; motion is the last 20-30° of extension.",
        clinical="Terminal extension drills for lockout strength and VMO function in knee rehab.",
        dosage="3 x 15 per leg"),
    dict(slug="wall-sit", name="Wall Sit",
        aliases=["wall squat hold", "static wall squat"],
        type="strength", movement="anti-extension", difficulty="beginner", position="standing",
        regions=[("knee", "primary"), ("hip", "secondary")],
        muscles=[("vastus-medialis", "primary"), ("rectus-femoris", "primary"),
                 ("vastus-lateralis", "primary"), ("gluteus-maximus", "stabilizer")],
        joints=[("knee-joint", "flexion"), ("patellofemoral-joint", "flexion")], equipment=["wall"],
        instructions=("1. Stand with your back to a wall, feet two shoe-lengths out.\n"
                      "2. Slide down until knees are bent ~45-60°, knees over ankles.\n"
                      "3. Hold, breathing steadily, back flat on the wall.\n"
                      "4. Build from 20 to 60 seconds."),
        breathing="Continuous; never hold.",
        safety="Keep thighs parallel; stop if pain under the kneecap is sharp.",
        dosage="3 x 30-45 seconds"),
    dict(slug="heel-slides", name="Heel Slides",
        aliases=["knee flexion heel slides", "heel slide knee mobility"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="supine",
        regions=[("knee", "primary")],
        muscles=[("biceps-femoris", "primary"),
                 ("popliteus", "secondary")],
        joints=[("knee-joint", "flexion")], equipment=["mat", "strap"],
        instructions=("1. Lie on your back, legs long.\n"
                      "2. Slowly slide one heel toward the buttocks, bending the knee.\n"
                      "3. Pause at the end of comfortable flexion for 3 seconds.\n"
                      "4. Slide back out; use a strap around the foot for assistance."),
        breathing="Exhale drawing the heel in.",
        safety="Smooth, pain-free arcs; use the strap rather than forcing.",
        clinical="Early knee-flexion ROM exercise after knee surgery or injury.",
        dosage="3 x 10-15 per leg"),
    dict(slug="patellar-mobilization", name="Patellar Mobilization",
        aliases=["kneecap mobilization", "patella glides"],
        type="physiotherapy", movement="gliding", difficulty="beginner", position="sitting",
        regions=[("knee", "primary")],
        muscles=[("patellar-tendon", "secondary")],
        joints=[("patellofemoral-joint", "gliding")], equipment=["chair"],
        instructions=("1. Sit with the knee straight and completely relaxed (foot supported).\n"
                      "2. Grip the kneecap edges and glide it gently up, down, inward and outward.\n"
                      "3. Hold each direction 5-10 seconds.\n"
                      "4. Keep the quad floppy — tension blocks the glide."),
        breathing="Relaxed exhales.",
        safety="The kneecap should move only millimetres; never force.",
        clinical="Used post knee surgery and in patellofemoral stiffness programmes.",
        dosage="10 gentle glides each direction"),
    dict(slug="popliteus-stretch", name="Popliteus Stretch (Soleus Bias)",
        aliases=["popliteal stretch", "bent-knee calf stretch for popliteus"],
        type="stretching", movement="dorsiflexion", difficulty="intermediate", position="standing",
        regions=[("knee", "primary"), ("calf", "secondary")],
        muscles=[("popliteus", "stretch_target"), ("soleus", "stretch_target")],
        joints=[("knee-joint", "flexion"), ("ankle-joint", "dorsiflexion")], equipment=["wall"],
        instructions=("1. Stand in a short lunge, hands on a wall, back knee slightly bent.\n"
                      "2. Keep the back heel down and rotate the back foot slightly inward.\n"
                      "3. Gently shift the back knee forward and across the midline.\n"
                      "4. Hold 20-30 seconds for a deep, behind-the-knee stretch."),
        breathing="Exhale into the shift.",
        safety="A stretch behind the knee should feel broad, never sharp or circular.",
        dosage="3 x 30 seconds per side"),
    dict(slug="itb-stretch-crossing", name="Standing ITB Cross-Over Stretch",
        aliases=["cross over ITB stretch", "standing iliotibial stretch"],
        type="stretching", movement="adduction", difficulty="beginner", position="standing",
        regions=[("hip", "primary"), ("knee", "secondary")],
        muscles=[("tensor-fasciae-latae", "stretch_target"), ("iliotibial-band", "stretch_target"),
                 ("gluteus-medius", "stretch_target")],
        joints=[("hip-joint", "adduction")], equipment=[],
        instructions=("1. Cross the leg to be stretched behind the other.\n"
                      "2. Side-bend the torso away, pushing the hip out.\n"
                      "3. Feel the band tighten along the outer hip to the knee.\n"
                      "4. Hold 20-30 seconds per side."),
        breathing="Relaxed.",
        safety="Keep the stretch along the outer thigh, not the low back.",
        dosage="2-3 x 30 seconds per side"),
]
