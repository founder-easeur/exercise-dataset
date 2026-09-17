"""Curated exercises: neck, jaw, shoulder, upper back.

Curated records are written and maintained by the Easeur team (origin=curated,
provenance origin=curated). They demonstrate the taxonomy depth — including
small structures like levator scapulae, suboccipitals, scalenes and the
individual rotator cuff muscles.
"""
from __future__ import annotations

NECK_SHOULDER_EXERCISES: list[dict] = [
    # ------------------------------------------------------------------ neck
    dict(slug="chin-tuck", name="Chin Tuck", aliases=["head retraction", "cervical retraction"],
        type="posture", movement="retraction", difficulty="beginner", position="seated or standing",
        regions=[("neck", "primary")],
        muscles=[("deep-neck-flexors", "primary"), ("cervical-extensors", "stretch_target")],
        joints=[("cervical-spine", "retraction")], equipment=[],
        instructions=("1. Sit or stand tall with your eyes on the horizon.\n"
                      "2. Gently draw your head straight back — as if making a double chin — without tilting up or down.\n"
                      "3. Hold for 3-5 seconds, feeling the deep front-neck muscles switch on.\n"
                      "4. Release slowly and repeat."),
        breathing="Exhale gently as you tuck; keep breathing steady throughout.",
        safety="Keep the motion small and pain-free; avoid forcing the head back with your hands.",
        contra="Avoid or reduce range if you feel dizziness, arm tingling or sharp pain.",
        clinical="Commonly used in physiotherapy programmes for forward-head posture and cervicogenic neck pain.",
        dosage="10 repetitions, 3-5 times per day"),
    dict(slug="deep-neck-flexor-activation", name="Deep Neck Flexor Activation",
        aliases=["craniocervical flexion", "deep cervical flexor exercise"],
        type="physiotherapy", movement="flexion", difficulty="beginner", position="supine",
        regions=[("neck", "primary")],
        muscles=[("deep-neck-flexors", "primary")],
        joints=[("cervical-spine", "flexion")], equipment=["mat"],
        instructions=("1. Lie on your back with a small towel under your head, knees bent.\n"
                      "2. Nod your head gently as if agreeing — a small, precise 'yes' motion.\n"
                      "3. Hold the nod for 5-10 seconds at a comfortable, low intensity.\n"
                      "4. Rest and repeat, keeping the superficial neck muscles relaxed."),
        breathing="Breathe slowly through the nose; do not hold your breath.",
        safety="Activation should feel subtle (about 20-30% effort), never straining.",
        contra="Stop if you experience dizziness or headache increase.",
        clinical="Cornerstone of cervical motor-control retraining used by physiotherapists.",
        dosage="10 x 10-second holds"),
    dict(slug="suboccipital-release", name="Suboccipital Release",
        aliases=["suboccipital muscle release", "base of skull release"],
        type="release", movement="extension", difficulty="beginner", position="supine",
        regions=[("neck", "primary")],
        muscles=[("suboccipitals", "stretch_target")],
        joints=[("cervical-spine", "extension")], equipment=["massage-ball", "mat"],
        instructions=("1. Lie on your back and place a pair of tennis balls in a sock at the base of your skull.\n"
                      "2. Let your head rest heavily onto the balls, eyes soft.\n"
                      "3. Breathe deeply for 1-2 minutes, allowing the suboccipitals to soften.\n"
                      "4. Small, slow 'yes' nods add a gentle mobilisation."),
        breathing="Slow diaphragmatic breathing; exhale to release further.",
        safety="Keep pressure moderate; never place balls on the top of the neck bones.",
        contra="Avoid with acute neck injury, severe osteoporosis or if it provokes dizziness.",
        clinical="Frequently included in programmes for cervicogenic and tension-type headache.",
        dosage="1-2 minutes"),
    dict(slug="suboccipital-stretch", name="Suboccipital Stretch",
        aliases=["skull base stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="seated",
        regions=[("neck", "primary")],
        muscles=[("suboccipitals", "stretch_target")],
        joints=[("cervical-spine", "flexion")], equipment=[],
        instructions=("1. Sit tall and interlace your fingers behind your head.\n"
                      "2. Allow your head to nod forward slightly, chin toward the ceiling-friendly tuck.\n"
                      "3. Let the weight of your arms apply a gentle traction at the skull base.\n"
                      "4. Hold 20-30 seconds, breathing easily."),
        breathing="Slow nasal breathing; soften on each exhale.",
        safety="Traction should be gentle — the arms cradle, they do not pull hard.",
        contra="Discontinue with arm numbness, tingling or dizziness.",
        dosage="3 x 30 seconds"),
    dict(slug="levator-scapulae-stretch", name="Levator Scapulae Stretch",
        aliases=["levator stretch", "levator scap stretch"],
        type="stretching", movement="lateral flexion", difficulty="beginner", position="seated",
        regions=[("neck", "primary"), ("shoulder", "secondary")],
        muscles=[("levator-scapulae", "stretch_target")],
        joints=[("cervical-spine", "rotation"), ("scapulothoracic-joint", "depression")],
        equipment=["chair"],
        instructions=("1. Sit on one hand (same side as the stretch) to anchor the shoulder blade.\n"
                      "2. Rotate your head 45° away from the anchored side, looking toward the opposite armpit.\n"
                      "3. With the free hand, gently guide the head diagonally forward and down.\n"
                      "4. Hold 20-30 seconds on each side."),
        breathing="Exhale as you deepen gently; never bounce.",
        safety="Keep the guide hand's pressure light — under 10% of your strength.",
        contra="Avoid after acute whiplash or with radiating arm symptoms.",
        dosage="3 x 30 seconds per side"),
    dict(slug="scalene-stretch", name="Scalene Stretch",
        aliases=["side neck stretch", "lateral neck stretch"],
        type="stretching", movement="lateral flexion", difficulty="beginner", position="seated",
        regions=[("neck", "primary")],
        muscles=[("scalenes", "stretch_target")],
        joints=[("cervical-spine", "lateral flexion")], equipment=[],
        instructions=("1. Sit tall and let one arm hang heavy to depress the shoulder.\n"
                      "2. Tilt your ear toward the opposite shoulder, keeping the face forward.\n"
                      "3. Rotate the head slightly upward and hold 20-30 seconds.\n"
                      "4. Repeat on the other side."),
        breathing="Steady, relaxed breathing throughout.",
        safety="Do not pull hard; the scalenes protect nerves and vessels of the neck.",
        contra="Stop immediately if you feel tingling down the arm or lightheadedness.",
        dosage="3 x 30 seconds per side"),
    dict(slug="upper-trap-stretch", name="Upper Trapezius Stretch",
        aliases=["upper trapezius stretch", "trapezius neck stretch"],
        type="stretching", movement="lateral flexion", difficulty="beginner", position="seated",
        regions=[("neck", "primary")],
        muscles=[("upper-trapezius", "stretch_target")],
        joints=[("cervical-spine", "lateral flexion")], equipment=[],
        instructions=("1. Anchor one hand under the thigh or behind the back.\n"
                      "2. Tilt your head to the opposite side, ear to shoulder.\n"
                      "3. Optionally turn the chin slightly toward the collarbone.\n"
                      "4. Apply light overpressure with the free hand; hold 20-30 seconds."),
        breathing="Relaxed; exhale into the stretch.",
        safety="Keep shoulders relaxed; avoid shrugging the stretching side.",
        contra="Use caution with any history of neck nerve symptoms.",
        dosage="3 x 30 seconds per side"),
    dict(slug="scm-stretch", name="Sternocleidomastoid Stretch",
        aliases=["SCM stretch"],
        type="stretching", movement="extension", difficulty="intermediate", position="seated",
        regions=[("neck", "primary")],
        muscles=[("sternocleidomastoid", "stretch_target")],
        joints=[("cervical-spine", "extension")], equipment=[],
        instructions=("1. Sit tall, looking forward.\n"
                      "2. Tilt your head back slightly and rotate it away from the side being stretched.\n"
                      "3. Feel the length along the front-side of the neck.\n"
                      "4. Hold 15-20 seconds and repeat on the other side."),
        breathing="Slow and even; avoid breath-holding with the head back.",
        safety="Keep extension mild; the throat should never feel compressed.",
        contra="Avoid with vertigo, cervical instability or vascular concerns.",
        dosage="3 x 20 seconds per side"),
    dict(slug="neck-rotation-stretch", name="Neck Rotation Stretch",
        aliases=["cervical rotation stretch", "neck turns", "neck rotation"],
        type="mobility", movement="rotation", difficulty="beginner", position="seated",
        regions=[("neck", "primary")],
        muscles=[("splenius-capitis", "stretch_target"), ("levator-scapulae", "secondary")],
        joints=[("cervical-spine", "rotation")], equipment=[],
        instructions=("1. Sit or stand tall with shoulders relaxed.\n"
                      "2. Slowly turn your head to one side, chin over the shoulder.\n"
                      "3. Hold 3-5 seconds at a comfortable end range, then return to centre.\n"
                      "4. Repeat to the other side, keeping the motion smooth."),
        breathing="Exhale as you rotate; inhale returning to centre.",
        safety="Rotate within comfort — no forcing or quick snapping motions.",
        contra="Reduce range with dizziness or if symptoms spread into the arm.",
        dosage="10 rotations per side"),
    dict(slug="cervical-extension-mobility", name="Cervical Extension Mobility",
        aliases=["neck look up", "cervical extension exercise"],
        type="mobility", movement="extension", difficulty="beginner", position="seated",
        regions=[("neck", "primary")],
        muscles=[("deep-neck-flexors", "stretch_target"), ("cervical-extensors", "primary")],
        joints=[("cervical-spine", "extension")], equipment=[],
        instructions=("1. Sit tall and slowly look up toward the ceiling.\n"
                      "2. Let the neck extend gently, mouth closed.\n"
                      "3. Pause 2-3 seconds, then return your gaze to eye level.\n"
                      "4. Repeat smoothly, one motion per 2-3 seconds."),
        breathing="Inhale as you look up; exhale returning.",
        safety="Keep the range comfortable; avoid if it provokes dizziness.",
        contra="Caution with spinal stenosis symptoms or balance issues.",
        dosage="8-10 repetitions"),
    dict(slug="prone-cervical-extension-endurance", name="Prone Cervical Extension Endurance",
        aliases=["prone neck extension", "neck extensor exercise"],
        type="physiotherapy", movement="extension", difficulty="beginner", position="prone",
        regions=[("neck", "primary")],
        muscles=[("cervical-extensors", "primary"), ("middle-trapezius", "stabilizer")],
        joints=[("cervical-spine", "extension")], equipment=["mat"],
        instructions=("1. Lie face down, forehead on a small folded towel.\n"
                      "2. Lift the head to align the neck with the spine — eyes to the floor.\n"
                      "3. Hold 5-10 seconds, keeping the shoulders heavy.\n"
                      "4. Lower with control and repeat."),
        breathing="Do not hold your breath; exhale during the lift.",
        safety="Lift only to neutral alignment, not beyond.",
        contra="Avoid with acute neck pain or extension-provoked symptoms.",
        dosage="10 x 10-second holds"),
    dict(slug="wall-posture-align", name="Wall Posture Alignment",
        aliases=["wall angels hold", "posture alignment"],
        type="posture", movement="extension", difficulty="beginner", position="standing",
        regions=[("neck", "primary"), ("upper-back", "secondary")],
        muscles=[("deep-neck-flexors", "primary"), ("middle-trapezius", "stabilizer"),
                 ("lower-trapezius", "stabilizer")],
        joints=[("thoracic-spine", "extension")], equipment=["wall"],
        instructions=("1. Stand with your heels, pelvis, upper back and head against a wall.\n"
                      "2. Perform a gentle chin tuck so the back of the head touches lightly.\n"
                      "3. Hold 20-30 seconds, breathing normally, feeling the tall stack.\n"
                      "4. Step away and try to keep the alignment for a minute."),
        breathing="Easy nasal breathing; ribs soft.",
        safety="If the head cannot comfortably reach the wall, keep the chin tuck alone.",
        contra=None,
        dosage="3 x 30 seconds"),
    dict(slug="neck-sidebend-mobility", name="Neck Side-Bend Mobility",
        aliases=["cervical lateral flexion mobility"],
        type="mobility", movement="lateral flexion", difficulty="beginner", position="seated",
        regions=[("neck", "primary")],
        muscles=[("scalenes", "stretch_target"), ("upper-trapezius", "stretch_target")],
        joints=[("cervical-spine", "lateral flexion")], equipment=[],
        instructions=("1. Sit tall, shoulders level.\n"
                      "2. Glide your ear toward one shoulder until the first comfortable stop.\n"
                      "3. Pause 2 seconds and return to centre.\n"
                      "4. Alternate sides in a slow rhythm."),
        breathing="Relaxed throughout.",
        safety="Keep shoulders still — the motion comes from the neck only.",
        contra="Reduce range with nerve symptoms.",
        dosage="8-10 per side"),
    dict(slug="thoracic-extension-foam-roll", name="Thoracic Extension Over Foam Roller",
        aliases=["t-spine extension", "foam roller thoracic extension"],
        type="mobility", movement="extension", difficulty="beginner", position="seated on floor",
        regions=[("upper-back", "primary"), ("chest", "secondary")],
        muscles=[("thoracic-erector-spinae", "stretch_target"), ("pectoralis-major", "stretch_target"),
                 ("pectoralis-minor", "stretch_target")],
        joints=[("thoracic-spine", "extension")], equipment=["foam-roller"],
        instructions=("1. Sit on the floor with a foam roller behind your mid back.\n"
                      "2. Support your head with your hands and extend over the roller.\n"
                      "3. Keep the ribs down — hinge at the thoracic spine, not the low back.\n"
                      "4. Move the roller an inch up the spine and repeat."),
        breathing="Inhale as you extend; exhale as you return.",
        safety="Never roll the neck or low back; stop at the bottom of the shoulder blades.",
        contra="Avoid with acute thoracic pain or known osteoporotic fracture risk.",
        dosage="5-8 segments, 2 passes"),
    # ------------------------------------------------------------------- jaw
    dict(slug="tmj-relaxed-jaw-position", name="TMJ Relaxed Jaw Position",
        aliases=["rest jaw position", "tongue on palate"],
        type="physiotherapy", movement=None, difficulty="beginner", position="seated",
        regions=[("jaw", "primary")],
        muscles=[("masseter", "secondary"), ("lateral-pterygoid", "stabilizer")],
        joints=[("temporomandibular-joint", "resting position")], equipment=[],
        instructions=("1. Rest the tongue gently on the roof of the mouth, lips closed, teeth apart.\n"
                      "2. Breathe through the nose, letting the jaw hang heavy.\n"
                      "3. Hold 1-2 minutes, noticing clenching habits melt away."),
        breathing="Slow nasal breathing, jaw unclenched.",
        safety="This is a relaxation exercise — there should be no effort.",
        contra=None,
        clinical="First-line self-care habit for temporomandibular disorder (TMD) management.",
        dosage="Several minutes, multiple times daily"),
    dict(slug="masseter-self-massage", name="Masseter Self-Massage",
        aliases=["jaw muscle massage", "cheek massage"],
        type="release", movement=None, difficulty="beginner", position="seated",
        regions=[("jaw", "primary")],
        muscles=[("masseter", "stretch_target"), ("temporalis", "secondary")],
        joints=[("temporomandibular-joint", "mobilisation")], equipment=[],
        instructions=("1. Find the masseter by clenching once, then relaxing, over the cheek angle.\n"
                      "2. Use knuckles or fingertips to make slow circles on the tight band.\n"
                      "3. Add gentle sustained pressure on tender spots for 20-30 seconds.\n"
                      "4. Finish with slow, relaxed jaw opening."),
        breathing="Slow and easy; soften the jaw on each exhale.",
        safety="Pressure should be comfortable, never sharp.",
        contra="Avoid over recently injured or surgically treated jaw areas.",
        dosage="2-3 minutes per side"),
    dict(slug="tmj-controlled-opening", name="TMJ Controlled Opening",
        aliases=["jaw controlled opening", "gentle jaw opening exercise"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="seated",
        regions=[("jaw", "primary")],
        muscles=[("lateral-pterygoid", "primary"), ("medial-pterygoid", "secondary"),
                 ("masseter", "secondary")],
        joints=[("temporomandibular-joint", "depression")], equipment=[],
        instructions=("1. Tongue on the palate, shoulders relaxed.\n"
                      "2. Open the mouth slowly and straight, as if yawning behind a mask.\n"
                      "3. Stop just before any click or deviation and close slowly.\n"
                      "4. Keep the motion mid-line, like a slow drawer."),
        breathing="Exhale on opening.",
        safety="Pain-free range only; never stretch into clicking.",
        clinical="Standard TMJ rehabilitation motor-control drill.",
        dosage="10 slow repetitions"),
    # -------------------------------------------------------------- shoulder
    dict(slug="sleeper-stretch", name="Sleeper Stretch",
        aliases=["side-lying internal rotation stretch"],
        type="stretching", movement="internal rotation", difficulty="intermediate", position="side-lying",
        regions=[("shoulder", "primary")],
        muscles=[("infraspinatus", "stretch_target"), ("teres-minor", "stretch_target")],
        joints=[("glenohumeral-joint", "internal rotation")], equipment=["mat"],
        instructions=("1. Lie on the stretch side with the arm at 90°, elbow level with the shoulder.\n"
                      "2. Use the top hand to gently press the forearm toward the floor.\n"
                      "3. Keep the shoulder blade pinned forward by rolling slightly onto it.\n"
                      "4. Hold 30 seconds at a mild stretch."),
        breathing="Exhale to soften into the position.",
        safety="Mild stretch only — this capsule tolerates low force.",
        contra="Avoid with shoulder instability or after certain repair surgeries without guidance.",
        clinical="Used in overhead-thrower programmes addressing glenohumeral internal rotation deficit (GIRD).",
        dosage="3-4 x 30 seconds per side"),
    dict(slug="cross-body-shoulder-stretch", name="Cross-Body Shoulder Stretch",
        aliases=["horizontal adduction stretch", "cross arm stretch"],
        type="stretching", movement="adduction", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary"), ("upper-back", "secondary")],
        muscles=[("infraspinatus", "stretch_target"), ("teres-minor", "stretch_target"),
                 ("deltoid-posterior", "stretch_target"), ("rhomboid-major", "secondary")],
        joints=[("glenohumeral-joint", "horizontal adduction")], equipment=[],
        instructions=("1. Bring one arm across your chest at shoulder height.\n"
                      "2. Hook the other forearm above the elbow and pull gently inward.\n"
                      "3. Keep the shoulder blade of the stretching arm from hiking up.\n"
                      "4. Hold 20-30 seconds each side."),
        breathing="Steady breathing, easing deeper on each exhale.",
        safety="Keep the elbow below shoulder height if the front of the shoulder pinches.",
        contra=None,
        dosage="3 x 30 seconds per side"),
    dict(slug="doorway-pec-stretch", name="Doorway Pectoral Stretch",
        aliases=["doorway chest stretch", "pectoral stretch doorway", "corner stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="standing",
        regions=[("chest", "primary"), ("shoulder", "secondary")],
        muscles=[("pectoralis-major", "stretch_target"), ("pectoralis-minor", "stretch_target")],
        joints=[("glenohumeral-joint", "external rotation"), ("scapulothoracic-joint", "retraction")],
        equipment=["doorway"],
        instructions=("1. Place your forearms on a door frame, elbows at shoulder height.\n"
                      "2. Step one foot forward into the doorway until a chest stretch appears.\n"
                      "3. Elbows lower bias the pec major; higher bias pec minor.\n"
                      "4. Hold 30 seconds, keeping ribs stacked over pelvis."),
        breathing="Inhale to lengthen the chest; exhale to settle deeper.",
        safety="Keep the stretch in the chest, not the shoulder front or low back.",
        contra=None,
        dosage="3 x 30 seconds"),
    dict(slug="pendulum-exercise", name="Pendulum Exercise",
        aliases=["codman pendulum", "shoulder pendulum swing"],
        type="rehabilitation", movement="circumduction", difficulty="beginner", position="standing bent over",
        regions=[("shoulder", "primary")],
        muscles=[("supraspinatus", "secondary"), ("deltoid-anterior", "stabilizer"),
                 ("deltoid-lateral", "stabilizer"), ("deltoid-posterior", "stabilizer")],
        joints=[("glenohumeral-joint", "circumduction")], equipment=["table", "chair"],
        instructions=("1. Lean on a table with the uninvolved arm, letting the other arm hang.\n"
                      "2. Relax the hanging arm completely and swing it in small circles.\n"
                      "3. Make 10 circles each direction, then gentle forward-back swings.\n"
                      "4. Let momentum, not muscle, do the work."),
        breathing="Relaxed; the arm must stay passive.",
        safety="Keep the torso still and the arm loose.",
        clinical="Early-stage shoulder rehabilitation for post-injury and post-surgical mobility.",
        dosage="10 circles each direction, several times daily"),
    dict(slug="band-external-rotation", name="Resistance Band External Rotation",
        aliases=["side-lying external rotation band", "rotator cuff external rotation"],
        type="physiotherapy", movement="external rotation", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary")],
        muscles=[("infraspinatus", "primary"), ("teres-minor", "primary")],
        joints=[("glenohumeral-joint", "external rotation")], equipment=["resistance-band", "towel"],
        instructions=("1. Hold a band with elbows bent 90° tucked at your sides; a rolled towel helps.\n"
                      "2. Keep elbows pinned and rotate both forearms outward against resistance.\n"
                      "3. Squeeze the shoulder blades gently back as you rotate.\n"
                      "4. Return slowly over 3 seconds."),
        breathing="Exhale rotating out; inhale returning.",
        safety="Use a light band — rotator cuffs respond to control, not load.",
        contra="Avoid pain at the top of motion; reduce resistance if form breaks.",
        clinical="Rotator-cuff strengthening staple for impingement-type shoulder programmes.",
        dosage="3 x 12-15, light band"),
    dict(slug="band-internal-rotation", name="Resistance Band Internal Rotation",
        aliases=["rotator cuff internal rotation band"],
        type="physiotherapy", movement="internal rotation", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary")],
        muscles=[("subscapularis", "primary"), ("pectoralis-major", "secondary")],
        joints=[("glenohumeral-joint", "internal rotation")], equipment=["resistance-band", "towel"],
        instructions=("1. Anchor a band at waist height beside you, elbow bent 90° at your side.\n"
                      "2. Rotate the forearm across your stomach against the resistance.\n"
                      "3. Keep the elbow glued to the ribs; move only at the shoulder.\n"
                      "4. Return slowly with control."),
        breathing="Exhale pulling in; inhale returning.",
        safety="Light resistance; stop if the front of the shoulder pinches.",
        dosage="3 x 12-15, light band"),
    dict(slug="scapular-retraction", name="Scapular Retraction",
        aliases=["shoulder blade squeeze", "scap squeeze"],
        type="posture", movement="retraction", difficulty="beginner", position="seated or standing",
        regions=[("upper-back", "primary"), ("shoulder", "secondary")],
        muscles=[("rhomboid-major", "primary"), ("rhomboid-minor", "primary"),
                 ("middle-trapezius", "primary")],
        joints=[("scapulothoracic-joint", "retraction")], equipment=[],
        instructions=("1. Sit or stand tall, arms relaxed at your sides.\n"
                      "2. Draw the shoulder blades together and slightly down, as if pinching a pencil.\n"
                      "3. Hold 5 seconds without shrugging.\n"
                      "4. Release slowly and repeat."),
        breathing="Exhale on the squeeze.",
        safety="Keep the neck long — no shrugging.",
        dosage="3 x 10, 5-second holds"),
    dict(slug="wall-slides", name="Wall Slides",
        aliases=["wall angels", "scapular wall slides"],
        type="mobility", movement="scapular upward rotation", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary"), ("upper-back", "secondary")],
        muscles=[("serratus-anterior", "primary"), ("lower-trapezius", "primary"),
                 ("lower-trapezius", "stabilizer")],
        joints=[("scapulothoracic-joint", "upward rotation"), ("glenohumeral-joint", "flexion")],
        equipment=["wall"],
        instructions=("1. Stand with back, head and wrists against a wall, elbows bent in a 'W'.\n"
                      "2. Slide the arms slowly up into a 'Y', keeping contact where possible.\n"
                      "3. Feel the shoulder blades rotating upward and outward.\n"
                      "4. Lower with the same control."),
        breathing="Exhale sliding up; inhale down.",
        safety="Keep the low back flat — the goal is scapular motion, not lumbar arching.",
        dosage="3 x 10 slow reps"),
    dict(slug="prone-y-raise", name="Prone Y Raise",
        aliases=["prone Y", "lower trap Y raise"],
        type="strength", movement="extension", difficulty="beginner", position="prone",
        regions=[("upper-back", "primary"), ("shoulder", "secondary")],
        muscles=[("lower-trapezius", "primary"), ("serratus-anterior", "secondary")],
        joints=[("scapulothoracic-joint", "upward rotation")], equipment=["mat"],
        instructions=("1. Lie face down, arms overhead in a Y, thumbs toward the ceiling.\n"
                      "2. Lift the arms a few centimetres, initiating from the shoulder blades.\n"
                      "3. Hold 2-3 seconds at the top without craning the neck.\n"
                      "4. Lower slowly and repeat."),
        breathing="Exhale lifting.",
        safety="Small range — this is a precision muscle, not a lifting drill.",
        dosage="3 x 10-12"),
    dict(slug="prone-t-raise", name="Prone T Raise",
        aliases=["prone T", "rhomboid T raise"],
        type="strength", movement="retraction", difficulty="beginner", position="prone",
        regions=[("upper-back", "primary")],
        muscles=[("rhomboid-major", "primary"), ("rhomboid-minor", "primary"),
                 ("middle-trapezius", "primary")],
        joints=[("scapulothoracic-joint", "retraction")], equipment=["mat"],
        instructions=("1. Lie face down, arms straight out to the sides, thumbs up.\n"
                      "2. Squeeze the shoulder blades to lift the arms into a T.\n"
                      "3. Hold 2-3 seconds, feeling the mid-back work.\n"
                      "4. Lower with control."),
        breathing="Exhale lifting.",
        safety="Keep the neck relaxed, forehead down.",
        dosage="3 x 10-12"),
    dict(slug="prone-w-raise", name="Prone W Raise",
        aliases=["prone W", "external rotation W"],
        type="strength", movement="external rotation", difficulty="beginner", position="prone",
        regions=[("shoulder", "primary"), ("upper-back", "secondary")],
        muscles=[("infraspinatus", "primary"), ("teres-minor", "primary"),
                 ("rhomboid-major", "secondary")],
        joints=[("glenohumeral-joint", "external rotation")], equipment=["mat"],
        instructions=("1. Lie face down, elbows bent in a W beside the ribs.\n"
                      "2. Rotate the arms to lift the backs of the hands toward the ceiling.\n"
                      "3. Keep the elbows lightly touching the sides.\n"
                      "4. Pause 2 seconds and lower slowly."),
        breathing="Exhale lifting.",
        safety="Lift only as high as pain-free rotator control allows.",
        dosage="3 x 10-12"),
    dict(slug="serratus-punch", name="Serratus Anterior Punch",
        aliases=["supine serratus punch", "scapular protraction punch"],
        type="physiotherapy", movement="protraction", difficulty="beginner", position="supine",
        regions=[("shoulder", "primary"), ("chest", "secondary")],
        muscles=[("serratus-anterior", "primary"), ("pectoralis-major", "secondary")],
        joints=[("scapulothoracic-joint", "protraction")], equipment=["mat", "dumbbell"],
        instructions=("1. Lie on your back, arms pointed at the ceiling.\n"
                      "2. Keeping the arms vertical, punch upward so the shoulder blades leave the floor.\n"
                      "3. Pause 2 seconds at the top, feeling the rib-side muscles.\n"
                      "4. Lower the shoulder blades slowly and repeat."),
        breathing="Exhale on the punch.",
        safety="Light or no weight to start; the motion is only a few centimetres.",
        clinical="Serratus activation drill for scapular dyskinesis programmes.",
        dosage="3 x 12"),
    dict(slug="wall-pushup-plus", name="Wall Push-Up Plus",
        aliases=["push up plus wall", "scapular plus pushup"],
        type="strength", movement="protraction", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary"), ("chest", "secondary")],
        muscles=[("serratus-anterior", "primary"), ("pectoralis-major", "primary"),
                 ("deltoid-anterior", "secondary")],
        joints=[("scapulothoracic-joint", "protraction")], equipment=["wall"],
        instructions=("1. Stand arm's length from a wall, hands at chest height.\n"
                      "2. Perform a push-up, then at the top push extra — spreading the shoulder blades apart.\n"
                      "3. Hold the 'plus' position 2 seconds.\n"
                      "4. Return with control."),
        breathing="Exhale pushing away.",
        safety="Keep the body in one line; the plus should feel like the ribs pushing forward.",
        dosage="3 x 10"),
    dict(slug="band-pull-apart", name="Band Pull-Apart",
        aliases=["resistance band pull apart"],
        type="strength", movement="retraction", difficulty="beginner", position="standing",
        regions=[("upper-back", "primary"), ("shoulder", "secondary")],
        muscles=[("rhomboid-major", "primary"), ("middle-trapezius", "primary"),
                 ("deltoid-posterior", "primary"), ("infraspinatus", "secondary")],
        joints=[("scapulothoracic-joint", "retraction")], equipment=["resistance-band"],
        instructions=("1. Hold a band at shoulder height, hands shoulder-width, palms down.\n"
                      "2. Pull the band apart to your chest, arms straight.\n"
                      "3. Squeeze the shoulder blades for 1-2 seconds.\n"
                      "4. Return slowly, keeping tension."),
        breathing="Exhale pulling.",
        safety="Choose a band that allows full range without shrugging.",
        dosage="3 x 15"),
    dict(slug="shoulder-flexion-wand", name="Shoulder Flexion Wand Exercise",
        aliases=["cane shoulder flexion", "overhead wand exercise"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="supine",
        regions=[("shoulder", "primary")],
        muscles=[("deltoid-anterior", "primary"), ("supraspinatus", "secondary")],
        joints=[("glenohumeral-joint", "flexion")], equipment=["stick", "mat"],
        instructions=("1. Lie on your back gripping a stick/broom wider than shoulders.\n"
                      "2. Use the healthy arm to help lift both arms overhead.\n"
                      "3. Guide to the highest comfortable point, elbows soft.\n"
                      "4. Lower with the good arm doing the braking."),
        breathing="Exhale lifting overhead.",
        safety="Assisted range only — never push through pinching.",
        clinical="Standard post-operative and frozen-shoulder assisted ROM progression.",
        dosage="10-15 repetitions"),
    dict(slug="towel-internal-rotation-stretch", name="Towel Internal Rotation Stretch",
        aliases=["behind-the-back towel stretch", "internal rotation towel stretch"],
        type="stretching", movement="internal rotation", difficulty="intermediate", position="standing",
        regions=[("shoulder", "primary")],
        muscles=[("subscapularis", "stretch_target")],
        joints=[("glenohumeral-joint", "internal rotation")], equipment=["towel"],
        instructions=("1. Drape a towel over the involved shoulder, holding the top end.\n"
                      "2. Reach behind your back with the other hand and grab the low end.\n"
                      "3. Pull the low end gently upward to stretch the back of the shoulder.\n"
                      "4. Hold 30 seconds at a mild intensity."),
        breathing="Exhale while pulling.",
        safety="Mild stretch only; the posterior capsule is sensitive.",
        clinical="A common post-surgical stiffness exercise, often after rotator cuff repair.",
        dosage="3-4 x 30 seconds"),
    dict(slug="arm-hangs", name="Dead Hang", aliases=["bar hang", "passive hang"],
        type="stretching", movement="elevation", difficulty="intermediate", position="standing",
        regions=[("shoulder", "primary"), ("chest", "secondary"), ("upper-back", "secondary")],
        muscles=[("latissimus-dorsi", "stretch_target"), ("teres-major", "stretch_target"),
                 ("pectoralis-major", "stretch_target")],
        joints=[("glenohumeral-joint", "flexion")], equipment=["table"],
        instructions=("1. Grip a stable bar or edge with an overhand grip.\n"
                      "2. Let the body hang with feet brushing the floor for safety.\n"
                      "3. Breathe deeply, letting the shoulders rise beside the ears.\n"
                      "4. Build from 10-second hangs."),
        breathing="Deep, relaxed breathing — the key to letting go.",
        safety="Keep feet available for support; disengage if the elbow or shoulder pinches.",
        contra="Avoid with shoulder instability symptoms or acute elbow complaints.",
        dosage="3-5 x 15-30 seconds"),
    dict(slug="eagle-arm-stretch", name="Eagle Arm Stretch",
        aliases=["cow face arms", "gomukhasana arms"],
        type="stretching", movement="external rotation", difficulty="intermediate", position="seated",
        regions=[("shoulder", "primary")],
        muscles=[("infraspinatus", "stretch_target"), ("teres-minor", "stretch_target"),
                 ("deltoid-posterior", "stretch_target"), ("rhomboid-major", "secondary")],
        joints=[("glenohumeral-joint", "internal rotation")], equipment=[],
        instructions=("1. Wrap one arm under the other, elbows crossing.\n"
                      "2. Press the palms together (or hold opposite shoulders).\n"
                      "3. Lift the elbows to shoulder height, sliding the top shoulder blade down.\n"
                      "4. Hold 30 seconds and unwind slowly."),
        breathing="Even, unhurried breathing.",
        safety="Take the wrap only as far as comfort allows — shoulders vary widely.",
        dosage="2 x 30 seconds per side"),
    dict(slug="scapular-clock", name="Scapular Clock",
        aliases=["shoulder blade clock"],
        type="mobility", movement="circumduction", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary")],
        muscles=[("serratus-anterior", "primary"), ("lower-trapezius", "primary"),
                 ("upper-trapezius", "stabilizer")],
        joints=[("scapulothoracic-joint", "circumduction")], equipment=["wall"],
        instructions=("1. Place a forearm on a wall at shoulder height.\n"
                      "2. Imagine a clock face on the wall and reach the shoulder blade toward 12, 3, 6 and 9.\n"
                      "3. Move slowly, isolating the shoulder blade from the arm.\n"
                      "4. Repeat both directions."),
        breathing="Relaxed breathing.",
        safety="Small, controlled reaches; the arm stays still.",
        dosage="2-3 rounds per side"),
    dict(slug="prone-on-elbows", name="Prone on Elbows",
        aliases=["sphinx position"],
        type="mobility", movement="extension", difficulty="beginner", position="prone",
        regions=[("upper-back", "primary"), ("lower-back", "secondary")],
        muscles=[("thoracic-erector-spinae", "stretch_target"), ("pectoralis-major", "stretch_target")],
        joints=[("thoracic-spine", "extension"), ("lumbar-spine", "extension")], equipment=["mat"],
        instructions=("1. Lie face down and rise onto your forearms, elbows under shoulders.\n"
                      "2. Let the chest sink forward while the shoulder blades draw together.\n"
                      "3. Keep the neck long; breathe into the upper chest.\n"
                      "4. Hold 20-30 seconds, or rock gently side to side."),
        breathing="Slow deep breaths to open the front of the chest.",
        safety="Keep the low back comfortable — bias the upper back by squeezing the blades.",
        dosage="3 x 30 seconds"),
    dict(slug="cat-cow", name="Cat-Cow",
        aliases=["cat camel", "spinal flexion extension quadruped"],
        type="mobility", movement="flexion", difficulty="beginner", position="quadruped",
        regions=[("upper-back", "primary"), ("lower-back", "primary")],
        muscles=[("thoracic-erector-spinae", "stretch_target"), ("lumbar-erector-spinae", "stretch_target"),
                 ("rectus-abdominis", "primary")],
        joints=[("thoracic-spine", "flexion"), ("lumbar-spine", "flexion")], equipment=["mat"],
        instructions=("1. Start on hands and knees, wrists under shoulders.\n"
                      "2. Exhale: round the spine to the ceiling, tucking the tailbone (cat).\n"
                      "3. Inhale: tilt the pelvis, open the chest and let the belly sink (cow).\n"
                      "4. Flow slowly between the two for 10 breaths."),
        breathing="Movement follows breath — exhale cat, inhale cow.",
        safety="Keep the range comfortable for the wrists and low back.",
        dosage="10 slow cycles"),
    dict(slug="thread-the-needle", name="Thread the Needle",
        aliases=["needle pose", "thoracic rotation stretch quadruped"],
        type="stretching", movement="rotation", difficulty="beginner", position="quadruped",
        regions=[("upper-back", "primary"), ("shoulder", "secondary")],
        muscles=[("thoracic-erector-spinae", "stretch_target"), ("rhomboid-major", "stretch_target"),
                 ("deltoid-posterior", "stretch_target")],
        joints=[("thoracic-spine", "rotation")], equipment=["mat"],
        instructions=("1. From hands and knees, slide one arm under the chest, palm up.\n"
                      "2. Lower the shoulder and temple toward the floor.\n"
                      "3. Breathe into the twist for 30 seconds.\n"
                      "4. Optionally reach the top arm overhead to deepen."),
        breathing="Long exhales unwind the rotation.",
        safety="Support the head with a cushion if the floor feels far.",
        dosage="2 x 30 seconds per side"),
    dict(slug="open-book-thoracic-rotation", name="Open Book Thoracic Rotation",
        aliases=["open books", "side-lying thoracic rotation"],
        type="mobility", movement="rotation", difficulty="beginner", position="side-lying",
        regions=[("upper-back", "primary"), ("chest", "secondary")],
        muscles=[("thoracic-erector-spinae", "stretch_target"), ("pectoralis-major", "stretch_target")],
        joints=[("thoracic-spine", "rotation"), ("glenohumeral-joint", "abduction")],
        equipment=["mat", "pillow"],
        instructions=("1. Lie on your side, knees stacked and hips at 90°, arms together at shoulder height.\n"
                      "2. Keeping knees glued, open the top arm like a book lid.\n"
                      "3. Follow the hand with the eyes until the shoulder blade nears the floor.\n"
                      "4. Breathe 3 deep breaths and close the book."),
        breathing="Inhale to open; exhale to soften deeper.",
        safety="Block the knees with a pillow; the low back should not roll.",
        dosage="8-10 per side"),
]
