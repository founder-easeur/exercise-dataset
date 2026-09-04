"""Curated exercises: whole-body recovery, warm-up and cool-down."""
from __future__ import annotations

GENERAL_EXERCISES: list[dict] = [
    dict(slug="arm-circles", name="Arm Circles",
        aliases=["shoulder circles", "dynamic arm swings"],
        type="warmup", movement="circumduction", difficulty="beginner", position="standing",
        regions=[("shoulder", "primary")],
        muscles=[("deltoid-anterior", "primary"), ("deltoid-lateral", "primary"),
                 ("deltoid-posterior", "primary"), ("serratus-anterior", "stabilizer")],
        joints=[("glenohumeral-joint", "circumduction"), ("scapulothoracic-joint", "circumduction")],
        equipment=[],
        instructions=("1. Stand tall, arms out to the sides.\n"
                      "2. Draw small circles forward, growing larger over 10 reps.\n"
                      "3. Reverse direction for 10 more.\n"
                      "4. Keep the neck relaxed and ribs stacked."),
        breathing="Rhythmic.",
        safety=None,
        dosage="10 each direction"),
    dict(slug="hip-circles-standing-large", name="Standing Large Hip Circles",
        aliases=["hip swings dynamic warmup", "large hip circles"],
        type="warmup", movement="circumduction", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("gluteus-maximus", "primary"), ("gluteus-medius", "primary"),
                 ("adductor-longus", "secondary"), ("iliopsoas", "secondary")],
        joints=[("hip-joint", "circumduction")], equipment=["wall"],
        instructions=("1. Stand on one leg, hands on a wall or rail.\n"
                      "2. Swing the free leg in the biggest relaxed circle possible.\n"
                      "3. 10 clockwise, 10 counter-clockwise.\n"
                      "4. Switch legs; stay tall and easy."),
        breathing="Continuous, easy.",
        safety="Circles grow with warmth; never force cold hips.",
        dosage="10 circles each direction per leg"),
    dict(slug="walking-hamstring-reach", name="Walking Hamstring Reach",
        aliases=["walking toe touch", "dynamic hamstring reach"],
        type="warmup", movement="flexion", difficulty="beginner", position="standing",
        regions=[("hip", "primary"), ("knee", "secondary")],
        muscles=[("biceps-femoris", "stretch_target"), ("semitendinosus", "stretch_target"),
                 ("semimembranosus", "stretch_target")],
        joints=[("hip-joint", "flexion")], equipment=[],
        instructions=("1. Walk two steps, then kick one leg straight ahead with the heel down.\n"
                      "2. Hinge the torso over the straight leg with a flat back.\n"
                      "3. Feel a brief hamstring stretch (2 seconds), stand tall.\n"
                      "4. Continue alternating for 10 reaches per leg."),
        breathing="Exhale on each reach.",
        safety="Dynamic, not ballistic — smooth reach, no bouncing.",
        dosage="10 per leg"),
    dict(slug="leg-swing-lateral", name="Lateral Leg Swings",
        aliases=["side-to-side leg swings", "dynamic adductor swings"],
        type="warmup", movement="adduction", difficulty="beginner", position="standing",
        regions=[("hip", "primary")],
        muscles=[("adductor-longus", "stretch_target"), ("adductor-magnus", "stretch_target"),
                 ("gluteus-medius", "stretch_target")],
        joints=[("hip-joint", "adduction"), ("hip-joint", "abduction")], equipment=["wall"],
        instructions=("1. Face a wall, both hands on it, weight on one leg.\n"
                      "2. Swing the free leg across the body and out to the side.\n"
                      "3. Keep the torso tall and the swing relaxed.\n"
                      "4. 15 swings, then switch legs."),
        breathing="Easy rhythm.",
        safety="Start small and grow the arc.",
        dosage="15 per leg"),
    dict(slug="world-greatest-stretch", name="World's Greatest Stretch",
        aliases=["lunge with rotation", "worlds greatest stretch"],
        type="warmup", movement="rotation", difficulty="intermediate", position="standing",
        regions=[("hip", "primary"), ("upper-back", "secondary"), ("ankle", "secondary")],
        muscles=[("iliopsoas", "stretch_target"), ("rectus-femoris", "stretch_target"),
                 ("thoracic-erector-spinae", "stretch_target"), ("gluteus-maximus", "secondary")],
        joints=[("hip-joint", "extension"), ("thoracic-spine", "rotation"),
                ("ankle-joint", "dorsiflexion")], equipment=["mat"],
        instructions=("1. Step into a long lunge, both hands inside the front foot.\n"
                      "2. Drop the back knee if needed; the front ankle stays deep.\n"
                      "3. Place one forearm down and rotate the other arm to the ceiling.\n"
                      "4. Hold 3 breaths; switch the rotation, then switch legs."),
        breathing="Inhale to rotate open; exhale to soften.",
        safety="Elevate hands on a block if the floor is far.",
        dosage="3 per side"),
    dict(slug="legs-up-the-wall", name="Legs Up the Wall",
        aliases=["viparita karani", "wall supported inversion rest"],
        type="recovery", movement=None, difficulty="beginner", position="supine",
        regions=[("whole-body", "primary"), ("hip", "secondary"), ("calf", "secondary")],
        muscles=[("iliopsoas", "stretch_target"), ("biceps-femoris", "stretch_target")],
        joints=[("hip-joint", "flexion")], equipment=["wall", "mat"],
        instructions=("1. Sit sideways against a wall and swing the legs up as you lie back.\n"
                      "2. Rest the heels on the wall, arms open, palms up.\n"
                      "3. Close the eyes and breathe slowly for 5-10 minutes.\n"
                      "4. Bend the knees and roll to the side to exit."),
        breathing="Slow, quiet nasal breathing.",
        safety="Keep a slight knee bend or move the hips away from the wall if hamstrings grip.",
        dosage="5-10 minutes"),
    dict(slug="supine-corpse-relaxation", name="Supine Relaxation (Savasana)",
        aliases=["corpse pose", "guided relaxation"],
        type="recovery", movement=None, difficulty="beginner", position="supine",
        regions=[("whole-body", "primary")],
        muscles=[("diaphragm", "primary")],
        joints=[], equipment=["mat", "pillow"],
        instructions=("1. Lie on your back, limbs comfortable and symmetrical, palms up.\n"
                      "2. Systematically relax: feet, calves, thighs, hips, belly, chest, arms, neck, face.\n"
                      "3. Let the breath be quiet and unforced.\n"
                      "4. Rest 5-15 minutes, staying awake but deeply calm."),
        breathing="Natural, quiet.",
        safety=None,
        dosage="5-15 minutes"),
    dict(slug="gentle-cool-down-walk", name="Gentle Cool-Down Walk",
        aliases=["cool down walk", "post-workout walk"],
        type="cooldown", movement=None, difficulty="beginner", position="standing",
        regions=[("whole-body", "primary"), ("calf", "secondary")],
        muscles=[("gastrocnemius", "secondary"), ("soleus", "secondary"),
                 ("gluteus-maximus", "secondary")],
        joints=[("ankle-joint", None), ("knee-joint", None), ("hip-joint", None)], equipment=[],
        instructions=("1. After hard exercise, drop to an easy conversational pace.\n"
                      "2. Walk 5-10 minutes, letting the breath settle.\n"
                      "3. Add long exhales: in through the nose, slowly out.\n"
                      "4. Finish with a full-body stretch of the day's tightest areas."),
        breathing="Nasal inhale, long exhale.",
        safety=None,
        dosage="5-10 minutes"),
    dict(slug="neck-to-ankle-scan", name="Body Scan Stretch Flow",
        aliases=["full body scan stretch", "head to toe stretch flow"],
        type="cooldown", movement=None, difficulty="beginner", position="standing",
        regions=[("whole-body", "primary")],
        muscles=[("upper-trapezius", "stretch_target"), ("latissimus-dorsi", "stretch_target"),
                 ("biceps-femoris", "stretch_target"), ("gastrocnemius", "stretch_target")],
        joints=[], equipment=["mat"],
        instructions=("1. From standing, roll down slowly and hang (knees soft).\n"
                      "2. Add gentle side reaches, then a lunge with a rotation.\n"
                      "3. Drop to a deep squat hold, then sit into a hamstring stretch each side.\n"
                      "4. Roll back up, finishing with 3 slow breaths standing tall."),
        breathing="Move on the exhale; one breath per position.",
        safety="Modify any position; the flow is a menu, not a test.",
        dosage="5 minutes"),
    dict(slug="standing-side-body-stretch", name="Standing Side Body Stretch",
        aliases=["standing side stretch", "crescent moon stretch"],
        type="stretching", movement="lateral flexion", difficulty="beginner", position="standing",
        regions=[("whole-body", "primary"), ("upper-back", "secondary")],
        muscles=[("latissimus-dorsi", "stretch_target"), ("obliques", "stretch_target"),
                 ("quadratus-lumborum", "stretch_target"), ("serratus-anterior", "secondary")],
        joints=[("lumbar-spine", "lateral flexion")], equipment=[],
        instructions=("1. Stand tall, interlace the fingers and reach overhead.\n"
                      "2. Arc gently to one side, hips even.\n"
                      "3. Breathe into the lengthening side for 20-30 seconds.\n"
                      "4. Return through centre and arc to the other side."),
        breathing="Direct breath into the open ribs.",
        safety=None,
        dosage="2 x 30 seconds per side"),
]
