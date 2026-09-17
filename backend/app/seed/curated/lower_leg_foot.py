"""Curated exercises: calf / shin, ankle, foot.

Emphasis on commonly-ignored structures: soleus, tibialis posterior,
peroneals, Achilles tendon, plantar fascia and intrinsic foot muscles.
"""
from __future__ import annotations

LOWER_LEG_FOOT_EXERCISES: list[dict] = [
    # ----------------------------------------------------------------- calf
    dict(slug="gastroc-wall-stretch", name="Gastrocnemius Wall Stretch",
        aliases=["straight knee calf stretch", "wall calf stretch", "runner's stretch"],
        type="stretching", movement="dorsiflexion", difficulty="beginner", position="standing",
        regions=[("calf", "primary"), ("ankle", "secondary")],
        muscles=[("gastrocnemius", "stretch_target"), ("plantaris", "stretch_target")],
        joints=[("ankle-joint", "dorsiflexion")], equipment=["wall"],
        instructions=("1. Face a wall in a staggered stance, hands on the wall.\n"
                      "2. Keep the back leg straight, heel pressed down, toes forward.\n"
                      "3. Shift forward until the calf stretches clearly.\n"
                      "4. Hold 30 seconds per leg."),
        breathing="Exhale to lean in.",
        safety="Keep the back heel grounded; heel lifting reduces the stretch.",
        dosage="3 x 30 seconds per side"),
    dict(slug="soleus-wall-stretch", name="Soleus Wall Stretch",
        aliases=["bent knee calf stretch", "soleus stretch"],
        type="stretching", movement="dorsiflexion", difficulty="beginner", position="standing",
        regions=[("calf", "primary"), ("ankle", "secondary")],
        muscles=[("soleus", "stretch_target"), ("tibialis-posterior", "stretch_target"),
                 ("flexor-digitorum-longus", "stretch_target"), ("flexor-hallucis-longus", "stretch_target")],
        joints=[("ankle-joint", "dorsiflexion"), ("subtalar-joint", "dorsiflexion")], equipment=["wall"],
        instructions=("1. Stand close to a wall, one foot back — this time with the back knee bent.\n"
                      "2. Keep the heel down and shift the back knee toward the wall.\n"
                      "3. The lower calf / Achilles area should stretch, not the upper calf.\n"
                      "4. Hold 30 seconds per side."),
        breathing="Steady.",
        safety="Bending the knee is the point — it isolates soleus over gastrocnemius.",
        clinical="Soleus length matters in Achilles tendinopathy and running-injury programmes.",
        dosage="3 x 30 seconds per side"),
    dict(slug="downward-dog-pedal", name="Downward Dog Pedaling",
        aliases=["pedaling heels downward dog", "adho mukha svanasasana calf stretch"],
        type="stretching", movement="dorsiflexion", difficulty="intermediate", position="standing bent over",
        regions=[("calf", "primary"), ("ankle", "secondary")],
        muscles=[("gastrocnemius", "stretch_target"), ("soleus", "stretch_target"),
                 ("achilles-tendon", "stretch_target")],
        joints=[("ankle-joint", "dorsiflexion")], equipment=["mat"],
        instructions=("1. From hands and knees, lift the hips into an inverted V.\n"
                      "2. Bend one knee, sending the opposite heel toward the floor.\n"
                      "3. Pedal the heels slowly, alternating for 20-30 seconds.\n"
                      "4. Finish with both heels reaching down."),
        breathing="Even breathing; keep the neck long.",
        safety="Bend the knees generously if the low back rounds.",
        dosage="30-45 seconds of pedaling"),
    dict(slug="eccentric-heel-drop", name="Eccentric Heel Drop (Alfredson)",
        aliases=["eccentric calf raise", "heel drop exercise", "alfredson protocol"],
        type="rehabilitation", movement="dorsiflexion", difficulty="intermediate", position="standing",
        regions=[("calf", "primary"), ("ankle", "secondary")],
        muscles=[("gastrocnemius", "primary"), ("soleus", "primary"),
                 ("achilles-tendon", "primary")],
        joints=[("ankle-joint", "plantarflexion")], equipment=["step"],
        instructions=("1. Stand on a step with the balls of the feet, heels hanging off.\n"
                      "2. Rise onto both tiptoes (use the healthy leg to help).\n"
                      "3. Shift weight to the involved leg and lower the heel below the step over 3-4 seconds.\n"
                      "4. Use the good leg to rise again; repeat."),
        breathing="Exhale on the slow lowering.",
        safety="Expect mild tendon discomfort; sharp pain means reduce range or load.",
        clinical="The Alfredson eccentric protocol — landmark rehabilitation programme for mid-portion Achilles tendinopathy.",
        dosage="3 x 15, twice daily (straight and bent knee)"),
    dict(slug="standing-calf-raise", name="Standing Calf Raise",
        aliases=["heel raise", "calf raise exercise", "double leg calf raise"],
        type="strength", movement="plantarflexion", difficulty="beginner", position="standing",
        regions=[("calf", "primary"), ("foot", "secondary")],
        muscles=[("gastrocnemius", "primary"), ("soleus", "primary"),
                 ("achilles-tendon", "primary"), ("tibialis-posterior", "secondary")],
        joints=[("ankle-joint", "plantarflexion")], equipment=["wall"],
        instructions=("1. Stand with the balls of the feet on flat ground, hand on a wall for balance.\n"
                      "2. Rise as high as possible onto the toes — a full heel lift.\n"
                      "3. Pause 1-2 seconds at the top.\n"
                      "4. Lower slowly over 3 seconds."),
        breathing="Exhale rising.",
        safety="Do them with a slight knee bend to bias soleus as a variation.",
        dosage="3 x 15-20"),
    dict(slug="tibialis-anterior-stretch", name="Tibialis Anterior Stretch",
        aliases=["front of shin stretch", "kneeling shin stretch"],
        type="stretching", movement="plantarflexion", difficulty="beginner", position="kneeling",
        regions=[("calf", "primary"), ("ankle", "secondary")],
        muscles=[("tibialis-anterior", "stretch_target"), ("extensor-digitorum-longus", "stretch_target"),
                 ("extensor-hallucis-longus", "stretch_target")],
        joints=[("ankle-joint", "plantarflexion")], equipment=["mat", "pillow"],
        instructions=("1. Kneel with the tops of the feet on the floor (cushion under the ankles).\n"
                      "2. Sit the hips gently back toward the heels, toes pointing back.\n"
                      "3. Feel the front-of-shin muscles lengthen.\n"
                      "4. Hold 20-30 seconds; use hands on the floor to control weight."),
        breathing="Slow breathing.",
        safety="Pad the ankles; come up if the knees or ankles complain.",
        dosage="2-3 x 30 seconds"),
    dict(slug="peroneal-stretch", name="Peroneal Stretch",
        aliases=["peroneus stretch", "lateral calf stretch inversion"],
        type="stretching", movement="inversion", difficulty="intermediate", position="seated",
        regions=[("calf", "primary"), ("ankle", "secondary")],
        muscles=[("peroneus-longus", "stretch_target"), ("peroneus-brevis", "stretch_target"),
                 ("peroneal-tendons", "stretch_target")],
        joints=[("ankle-joint", "inversion"), ("subtalar-joint", "inversion")], equipment=["mat"],
        instructions=("1. Sit with one leg crossed over the other knee.\n"
                      "2. Hold the foot and gently draw it into inversion — sole turning inward/up.\n"
                      "3. Add slight plantarflexion to deepen the outer-leg stretch.\n"
                      "4. Hold 20-30 seconds per side."),
        breathing="Relaxed.",
        safety="Gentle — the peroneals cross a mobile joint.",
        dosage="3 x 25 seconds per side"),
    dict(slug="calf-foam-roll", name="Calf Foam Roll",
        aliases=["foam roller calf", "gastrocnemius foam rolling"],
        type="release", movement=None, difficulty="beginner", position="seated on floor",
        regions=[("calf", "primary")],
        muscles=[("gastrocnemius", "stretch_target"), ("soleus", "stretch_target"),
                 ("tibialis-posterior", "stretch_target")],
        joints=[], equipment=["foam-roller"],
        instructions=("1. Sit on the floor with the calf on a roller, hands behind for support.\n"
                      "2. Roll slowly from ankle to the back of the knee.\n"
                      "3. Rotate the leg in and out to reach the inner and outer calf.\n"
                      "4. Pause 20-30 seconds on tender spots; circle the ankle while paused."),
        breathing="Long exhales on knots.",
        safety="Avoid the back of the knee pit itself.",
        dosage="1-2 minutes per calf"),
    # ---------------------------------------------------------------- ankle
    dict(slug="ankle-circles", name="Ankle Circles",
        aliases=["ankle rotations", "ankle mobility circles"],
        type="mobility", movement="circumduction", difficulty="beginner", position="seated",
        regions=[("ankle", "primary"), ("foot", "secondary")],
        muscles=[("tibialis-anterior", "primary"), ("peroneus-longus", "primary"),
                 ("tibialis-posterior", "stabilizer")],
        joints=[("ankle-joint", "circumduction"), ("subtalar-joint", "circumduction")], equipment=["chair"],
        instructions=("1. Sit with the foot lifted slightly off the floor.\n"
                      "2. Circle the ankle slowly — 10 each direction.\n"
                      "3. Make the circles as large as the joint allows.\n"
                      "4. Point and flex the foot between sets."),
        breathing="Relaxed.",
        safety=None,
        dosage="10 circles each direction per ankle"),
    dict(slug="ankle-alphabet", name="Ankle Alphabet",
        aliases=["ankle ABCs", "alphabet ankle mobility"],
        type="mobility", movement="circumduction", difficulty="beginner", position="seated",
        regions=[("ankle", "primary")],
        muscles=[("tibialis-anterior", "primary"), ("peroneus-longus", "primary"),
                 ("extensor-digitorum-longus", "secondary")],
        joints=[("ankle-joint", "circumduction"), ("subtalar-joint", "circumduction")], equipment=["chair"],
        instructions=("1. Sit with one foot lifted.\n"
                      "2. Trace each letter of the alphabet in the air with the big toe.\n"
                      "3. Move slowly and make large letters.\n"
                      "4. Repeat with the other foot."),
        breathing="Easy.",
        safety=None,
        clinical="Common early-home-rehab mobility drill after ankle sprain.",
        dosage="A-Z per ankle"),
    dict(slug="knee-to-wall-ankle-mobility", name="Knee-to-Wall Ankle Mobility",
        aliases=["ankle dorsiflexion mobility", "knee to wall test exercise"],
        type="mobility", movement="dorsiflexion", difficulty="beginner", position="kneeling",
        regions=[("ankle", "primary"), ("knee", "secondary")],
        muscles=[("soleus", "stretch_target"), ("gastrocnemius", "secondary")],
        joints=[("ankle-joint", "dorsiflexion")], equipment=["wall"],
        instructions=("1. Place the toes of one foot a hand-width from a wall.\n"
                      "2. Keep the heel down and drive the knee straight toward the wall.\n"
                      "3. If the knee touches easily, move the foot back a centimetre and repeat.\n"
                      "4. Find the edge of range; 10-15 pumps per ankle."),
        breathing="Rhythmic.",
        safety="The heel must stay glued down — that's the measurement and the stretch.",
        clinical="Dorsiflexion deficit after ankle sprain is a re-injury risk factor; this is the standard self-mobilisation.",
        dosage="2 x 10-15 per ankle"),
    dict(slug="ankle-inversion-stretch", name="Ankle Inversion Stretch",
        aliases=["ankle inversion mobility", "inner ankle stretch"],
        type="mobility", movement="inversion", difficulty="beginner", position="seated",
        regions=[("ankle", "primary")],
        muscles=[("peroneus-longus", "stretch_target"), ("peroneus-brevis", "stretch_target"),
                 ("peroneal-tendons", "stretch_target")],
        joints=[("subtalar-joint", "inversion"), ("ankle-joint", "inversion")], equipment=["chair"],
        instructions=("1. Sit with the ankle resting on the opposite knee.\n"
                      "2. Cup the heel and turn the sole of the foot upward and inward.\n"
                      "3. Move into the comfortable end range, hold 5 seconds, release.\n"
                      "4. Repeat 10 times per ankle."),
        breathing="Relaxed.",
        safety="Post-sprain stiffness improves slowly; never force past pinching.",
        dosage="10 x 5-second holds per ankle"),
    dict(slug="band-ankle-eversion", name="Resistance Band Ankle Eversion",
        aliases=["peroneal strengthening band", "ankle eversion exercise"],
        type="rehabilitation", movement="eversion", difficulty="beginner", position="seated",
        regions=[("ankle", "primary"), ("calf", "secondary")],
        muscles=[("peroneus-longus", "primary"), ("peroneus-brevis", "primary"),
                 ("peroneal-tendons", "primary")],
        joints=[("subtalar-joint", "eversion"), ("ankle-joint", "eversion")],
        equipment=["resistance-band", "chair"],
        instructions=("1. Loop a band around the mid-foot and anchor it to the inside leg of a table (or hold it).\n"
                      "2. Keep the leg still and rotate the sole of the foot outward against the band.\n"
                      "3. Pause 1 second, return slowly.\n"
                      "4. Keep the motion at the ankle — the knee doesn't move."),
        breathing="Exhale everting.",
        safety="Light band; high reps build tendon tolerance.",
        clinical="Peroneal strengthening is central to lateral ankle sprain rehabilitation.",
        dosage="3 x 15 per ankle"),
    dict(slug="band-ankle-inversion", name="Resistance Band Ankle Inversion",
        aliases=["ankle inversion band exercise", "tibialis posterior band exercise"],
        type="rehabilitation", movement="inversion", difficulty="beginner", position="seated",
        regions=[("ankle", "primary"), ("calf", "secondary")],
        muscles=[("tibialis-posterior", "primary"), ("flexor-digitorum-longus", "secondary"),
                 ("flexor-hallucis-longus", "secondary")],
        joints=[("subtalar-joint", "inversion"), ("ankle-joint", "inversion")],
        equipment=["resistance-band", "chair"],
        instructions=("1. Sit with the band around the mid-foot, anchored to the outside.\n"
                      "2. Draw the sole of the foot inward and up against the band.\n"
                      "3. Keep the ankle at ~90°; the heel may lift slightly.\n"
                      "4. Return with control."),
        breathing="Exhale inverting.",
        safety="Light resistance; smooth tempo.",
        clinical="Tibialis posterior strengthening for posterior tibial tendon dysfunction and flat-foot care.",
        dosage="3 x 15 per ankle"),
    dict(slug="band-ankle-dorsiflexion", name="Resistance Band Ankle Dorsiflexion",
        aliases=["tibialis anterior band exercise", "dorsiflexion band exercise"],
        type="rehabilitation", movement="dorsiflexion", difficulty="beginner", position="seated",
        regions=[("calf", "primary"), ("ankle", "primary")],
        muscles=[("tibialis-anterior", "primary"), ("extensor-digitorum-longus", "secondary"),
                 ("extensor-hallucis-longus", "secondary")],
        joints=[("ankle-joint", "dorsiflexion")], equipment=["resistance-band", "chair"],
        instructions=("1. Anchor a band around the top of the foot, held in front.\n"
                      "2. Pull the toes and foot up toward the shin against resistance.\n"
                      "3. Keep the heel planted; only the ankle moves.\n"
                      "4. Lower slowly."),
        breathing="Exhale pulling up.",
        safety=None,
        dosage="3 x 15 per ankle"),
    dict(slug="single-leg-balance", name="Single-Leg Balance",
        aliases=["single leg stance", "one leg balance exercise"],
        type="balance", movement=None, difficulty="beginner", position="standing",
        regions=[("ankle", "primary"), ("foot", "primary"), ("hip", "secondary")],
        muscles=[("tibialis-posterior", "stabilizer"), ("peroneus-longus", "stabilizer"),
                 ("gluteus-medius", "stabilizer"), ("flexor-digitorum-longus", "stabilizer")],
        joints=[("ankle-joint", None), ("subtalar-joint", None)], equipment=["wall"],
        instructions=("1. Stand near a wall for safety and lift one foot.\n"
                      "2. Balance on the other leg with a soft, tall posture.\n"
                      "3. Aim for 30 seconds; harder = eyes closed or uneven surface.\n"
                      "4. Repeat 3 times per leg."),
        breathing="Quiet, steady breathing.",
        safety="Fingertip support first; progress by removing it.",
        clinical="Proprioceptive training reduces recurrent ankle sprain risk.",
        dosage="3 x 30 seconds per leg"),
    dict(slug="single-leg-balance-eyes-closed", name="Single-Leg Balance (Eyes Closed)",
        aliases=["eyes closed balance", "blind balance exercise"],
        type="balance", movement=None, difficulty="intermediate", position="standing",
        regions=[("ankle", "primary"), ("foot", "primary")],
        muscles=[("tibialis-posterior", "stabilizer"), ("peroneus-longus", "stabilizer"),
                 ("abductor-hallucis", "stabilizer"), ("flexor-digitorum-brevis", "stabilizer")],
        joints=[("ankle-joint", None), ("subtalar-joint", None)], equipment=["wall"],
        instructions=("1. Stand on one leg near a wall, then close the eyes.\n"
                      "2. Feel the foot and ankle making rapid small corrections.\n"
                      "3. Balance up to 30 seconds; open eyes if you tip.\n"
                      "4. Repeat 3 times per leg."),
        breathing="Calm and slow.",
        safety="Always within arm's reach of a wall.",
        dosage="3 x 20-30 seconds per leg"),
    # ----------------------------------------------------------------- foot
    dict(slug="plantar-fascia-ball-massage", name="Plantar Fascia Ball Massage",
        aliases=["golf ball roll", "plantar fascia massage", "foot ball rolling"],
        type="release", movement=None, difficulty="beginner", position="seated or standing",
        regions=[("foot", "primary")],
        muscles=[("plantar-fascia", "stretch_target"), ("flexor-digitorum-brevis", "stretch_target"),
                 ("abductor-hallucis", "secondary")],
        joints=[("midfoot-joints", None)], equipment=["massage-ball", "chair"],
        instructions=("1. Place a ball (tennis/golf) under the arch of the foot while seated.\n"
                      "2. Roll slowly from heel to the ball of the foot.\n"
                      "3. Pause 15-20 seconds on tender spots; flex the toes there.\n"
                      "4. Spend 1-2 minutes per foot."),
        breathing="Slow; soften on exhale.",
        safety="Seated pressure first; standing adds much more intensity.",
        clinical="First-line self-care for plantar fascia pain, especially before first steps in the morning.",
        dosage="1-2 minutes per foot"),
    dict(slug="plantar-fascia-stretch", name="Plantar Fascia Stretch",
        aliases=["towel stretch plantar fascia", "arch stretch", "toe pull stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="seated",
        regions=[("foot", "primary")],
        muscles=[("plantar-fascia", "stretch_target"), ("abductor-hallucis", "stretch_target"),
                 ("flexor-hallucis-brevis", "stretch_target")],
        joints=[("toe-mtp-joints", "extension")], equipment=["chair"],
        instructions=("1. Sit with the affected foot crossed over the knee.\n"
                      "2. Pull the toes back toward the shin until the arch tightens like a string.\n"
                      "3. With the other thumb, massage the taut arch gently.\n"
                      "4. Hold 10 seconds x 10 reps — best done before standing in the morning."),
        breathing="Relaxed.",
        safety=None,
        clinical="Strongly evidence-supported self-stretch for plantar heel pain.",
        dosage="10 x 10-second holds per foot"),
    dict(slug="toe-towel-scrunch", name="Toe Towel Scrunch",
        aliases=["towel curls", "towel crunch exercise"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="seated",
        regions=[("foot", "primary")],
        muscles=[("flexor-digitorum-brevis", "primary"), ("abductor-hallucis", "primary"),
                 ("lumbricals-foot", "primary"), ("interossei-foot", "primary")],
        joints=[("toe-mtp-joints", "flexion")], equipment=["towel", "chair"],
        instructions=("1. Sit with a flat towel on the floor under one foot.\n"
                      "2. Keeping the heel planted, scrunch the towel toward you with the toes.\n"
                      "3. Gather, release, and repeat until the towel is bunched.\n"
                      "4. Smooth it out and repeat; change feet."),
        breathing="Easy.",
        safety="Cramping is common at first — rest and continue.",
        clinical="Intrinsic foot muscle strengthening for arch support and plantar fascia programmes.",
        dosage="2-3 rounds per foot"),
    dict(slug="toe-yoga", name="Toe Yoga",
        aliases=["toe spread lift exercise", "big toe lift exercise"],
        type="mobility", movement="extension", difficulty="beginner", position="standing",
        regions=[("foot", "primary")],
        muscles=[("abductor-hallucis", "primary"), ("flexor-hallucis-brevis", "primary"),
                 ("extensor-digitorum-brevis", "secondary"), ("interossei-foot", "primary")],
        joints=[("toe-mtp-joints", "extension"), ("toe-mtp-joints", "flexion")], equipment=[],
        instructions=("1. Stand or sit with feet flat, weight even.\n"
                      "2. Lift only the big toes, keeping the other four down.\n"
                      "3. Then press the big toes down and lift the four lesser toes.\n"
                      "4. Alternate slowly 10-15 times, feet flat throughout."),
        breathing="Relaxed.",
        safety="It's fine if coordination is clumsy at first — that's the point.",
        clinical="Dissociated toe control trains intrinsic foot muscles for arch control.",
        dosage="2 x 10-15 cycles"),
    dict(slug="short-foot-exercise", name="Short Foot Exercise",
        aliases=["foot doming", "arch lift exercise"],
        type="rehabilitation", movement=None, difficulty="intermediate", position="standing",
        regions=[("foot", "primary")],
        muscles=[("abductor-hallucis", "primary"), ("flexor-hallucis-brevis", "primary"),
                 ("interossei-foot", "primary"), ("tibialis-posterior", "stabilizer")],
        joints=[("midfoot-joints", None)], equipment=[],
        instructions=("1. Stand barefoot with the foot flat, toes relaxed and straight.\n"
                      "2. Without curling the toes, draw the ball of the big toe toward the heel.\n"
                      "3. The arch domes up; the foot 'shortens'.\n"
                      "4. Hold 5-8 seconds; keep the ankle neutral."),
        breathing="Breathe normally; no toe gripping.",
        safety="If the toes curl or the ankle rolls out, restart smaller.",
        clinical="Evidence-supported intrinsic foot muscle exercise, used for flat foot and plantar fascia programmes.",
        dosage="3 x 8 per foot"),
    dict(slug="big-toe-stretch", name="Big Toe Stretch",
        aliases=["hallux stretch", "first MTP stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="kneeling",
        regions=[("foot", "primary")],
        muscles=[("flexor-hallucis-brevis", "stretch_target"), ("abductor-hallucis", "stretch_target"),
                 ("adductor-hallucis", "stretch_target")],
        joints=[("toe-mtp-joints", "extension")], equipment=["mat"],
        instructions=("1. Kneel in a lunge with the big toe of the back foot tucked under.\n"
                      "2. Gently sit the hips toward the heel, extending the big toe.\n"
                      "3. Keep the other four toes relaxed on the floor.\n"
                      "4. Hold 20-30 seconds; the base of the big toe should stretch."),
        breathing="Slow.",
        safety="Progress over weeks; the joint adapts gradually.",
        clinical="First MTP extension matters for walking mechanics and hallux rigidus care.",
        dosage="2-3 x 30 seconds per foot"),
    dict(slug="toe-spreader-stretch", name="Seated Toe Spreader Stretch",
        aliases=["toe spread stretch", "interdigital stretch"],
        type="stretching", movement="abduction", difficulty="beginner", position="seated",
        regions=[("foot", "primary")],
        muscles=[("interossei-foot", "stretch_target"),
                 ("abductor-hallucis", "stretch_target"), ("abductor-digiti-minimi", "stretch_target")],
        joints=[("toe-mtp-joints", "abduction")], equipment=["chair"],
        instructions=("1. Sit with the foot on the opposite knee.\n"
                      "2. Interlace the fingers of the opposite hand between the toes.\n"
                      "3. Gently rotate and spread for 20-30 seconds.\n"
                      "4. Repeat once more per foot."),
        breathing="Relaxed.",
        safety="Be extra gentle with the little toes.",
        dosage="2 x 30 seconds per foot"),
    dict(slug="intrinsic-heel-raise", name="Intrinsic-Offloaded Heel Raise",
        aliases=["toes-off heel raise", "big toe pressed heel raise"],
        type="strength", movement="plantarflexion", difficulty="intermediate", position="standing",
        regions=[("foot", "primary"), ("calf", "secondary")],
        muscles=[("flexor-hallucis-brevis", "primary"), ("abductor-hallucis", "primary"),
                 ("tibialis-posterior", "primary"), ("soleus", "secondary")],
        joints=[("ankle-joint", "plantarflexion"), ("toe-mtp-joints", "flexion")],
        equipment=["wall"],
        instructions=("1. Stand near a wall with the big toes pressed gently into the floor.\n"
                      "2. Keeping that pressure, rise to the heels' tops.\n"
                      "3. The arch stays domed and the toes stay long — no clawing.\n"
                      "4. Lower over 3 seconds."),
        breathing="Exhale rising.",
        safety="Quality of arch doming is the goal; lower the height if toes claw.",
        dosage="3 x 12"),
    dict(slug="toe-extensor-stretch", name="Toe Extensor Stretch",
        aliases=["top of foot stretch", "extensor digitorum stretch"],
        type="stretching", movement="plantarflexion", difficulty="beginner", position="kneeling",
        regions=[("foot", "primary"), ("ankle", "secondary")],
        muscles=[("extensor-digitorum-brevis", "stretch_target"), ("tibialis-anterior", "stretch_target"),
                 ("extensor-hallucis-longus", "stretch_target")],
        joints=[("toe-mtp-joints", "flexion"), ("ankle-joint", "plantarflexion")], equipment=["mat", "pillow"],
        instructions=("1. Kneel with the tops of the toes tucked under (cushion under the ankles).\n"
                      "2. Sit the hips back slightly, pointing the toes down.\n"
                      "3. The tops of the feet and toes stretch.\n"
                      "4. Hold 20-30 seconds gently."),
        breathing="Slow.",
        safety="Mild intensity; the small toe joints adapt slowly.",
        dosage="2 x 30 seconds"),
    dict(slug="ankle-dorsiflexion-stretch-kneeling", name="Kneeling Ankle Dorsiflexion Stretch",
        aliases=["kneeling ankle stretch", "deep ankle stretch"],
        type="stretching", movement="dorsiflexion", difficulty="beginner", position="kneeling",
        regions=[("ankle", "primary"), ("foot", "secondary")],
        muscles=[("soleus", "stretch_target"), ("achilles-tendon", "stretch_target")],
        joints=[("ankle-joint", "dorsiflexion")], equipment=["mat"],
        instructions=("1. Kneel on one knee with the front foot flat.\n"
                      "2. Shift the front knee far forward over or past the toes, heel down.\n"
                      "3. Pause at the deepest comfortable angle for 3-5 seconds.\n"
                      "4. Return and repeat 10 times per ankle."),
        breathing="Exhale shifting forward.",
        safety="Keep the foot flat and the arch from collapsing inward.",
        dosage="2 x 10 per side"),
    dict(slug="tibialis-posterior-ball-release", name="Tibialis Posterior Self-Release",
        aliases=["inner calf release", "posterior tibialis release"],
        type="release", movement=None, difficulty="intermediate", position="seated on floor",
        regions=[("calf", "primary"), ("foot", "secondary")],
        muscles=[("tibialis-posterior", "stretch_target"), ("flexor-digitorum-longus", "stretch_target"),
                 ("flexor-hallucis-longus", "stretch_target")],
        joints=[], equipment=["massage-ball"],
        instructions=("1. Sit with a ball tucked behind the inner shin bone, above the ankle.\n"
                      "2. Press the calf into the ball and slide slowly up the inner calf.\n"
                      "3. Pause on tender spots for 20-30 seconds; circle the foot while paused.\n"
                      "4. Work the inner calf in 3-4 lines."),
        breathing="Slow breathing.",
        safety="Stay on muscle, off the sharp shin bone edge.",
        dosage="1-2 minutes per leg"),
    dict(slug="marble-toe-pickup", name="Towel-Marble Combo Pickup",
        aliases=["marble pickup foot", "object pickup toes"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="standing",
        regions=[("foot", "primary")],
        muscles=[("flexor-digitorum-brevis", "primary"), ("lumbricals-foot", "primary"),
                 ("flexor-hallucis-brevis", "primary")],
        joints=[("toe-mtp-joints", "flexion")], equipment=["marbles"],
        instructions=("1. Place marbles on the floor before a chair, a cup beside them.\n"
                      "2. Using only the toes of one foot, pick up marbles into the cup.\n"
                      "3. Ten marbles per foot; alternate feet.\n"
                      "4. Progress by doing it standing on one leg."),
        breathing="Relaxed.",
        safety=None,
        dosage="10 pickups per foot"),
]
