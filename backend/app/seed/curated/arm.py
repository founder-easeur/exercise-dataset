"""Curated exercises: elbow, forearm, wrist, hand.

Includes the commonly-overlooked forearm compartments, the common
flexor/extensor tendons (golfer's/tennis elbow), the thumb compartment and
neural glides — structures standard exercise libraries miss.
"""
from __future__ import annotations

ARM_EXERCISES: list[dict] = [
    # ------------------------------------------------------------- forearm
    dict(slug="wrist-extensor-stretch", name="Wrist Extensor Stretch",
        aliases=["tennis elbow stretch", "straight arm wrist flexion stretch"],
        type="stretching", movement="flexion", difficulty="beginner", position="standing",
        regions=[("forearm", "primary"), ("wrist", "primary")],
        muscles=[("extensor-carpi-radialis", "stretch_target"), ("extensor-carpi-ulnaris", "stretch_target"),
                 ("extensor-digitorum", "stretch_target"), ("common-extensor-tendon", "stretch_target"),
                 ("brachioradialis", "secondary")],
        joints=[("wrist-joint", "flexion"), ("elbow-joint", "extension")], equipment=[],
        instructions=("1. Extend one arm straight in front, palm down.\n"
                      "2. With the other hand, bend the wrist down so fingers point to the floor.\n"
                      "3. Keep the elbow straight and shoulder relaxed.\n"
                      "4. Hold 20-30 seconds at a mild stretch along the outer forearm."),
        breathing="Relaxed; soften on each exhale.",
        safety="Mild intensity — tendons respond poorly to aggressive stretching.",
        clinical="First-line flexibility exercise in lateral epicondylitis (tennis elbow) self-care.",
        dosage="3 x 30 seconds per side"),
    dict(slug="wrist-flexor-stretch", name="Wrist Flexor Stretch",
        aliases=["golfer's elbow stretch", "straight arm wrist extension stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="standing",
        regions=[("forearm", "primary"), ("wrist", "primary")],
        muscles=[("flexor-carpi-radialis", "stretch_target"), ("flexor-carpi-ulnaris", "stretch_target"),
                 ("flexor-digitorum-superficialis", "stretch_target"), ("common-flexor-tendon", "stretch_target"),
                 ("palmaris-longus", "stretch_target")],
        joints=[("wrist-joint", "extension"), ("elbow-joint", "extension")], equipment=[],
        instructions=("1. Extend one arm straight, palm up.\n"
                      "2. With the other hand, bend the wrist back so fingers point to the ceiling.\n"
                      "3. Keep the elbow straight, stretching the inner forearm.\n"
                      "4. Hold 20-30 seconds gently."),
        breathing="Even breathing; no bouncing.",
        safety="Mild stretch only.",
        clinical="Used in medial epicondylitis (golfer's elbow) management.",
        dosage="3 x 30 seconds per side"),
    dict(slug="eccentric-wrist-extension", name="Eccentric Wrist Extension",
        aliases=["eccentric tennis elbow exercise", "reverse wrist curl eccentric"],
        type="rehabilitation", movement="extension", difficulty="beginner", position="seated",
        regions=[("forearm", "primary")],
        muscles=[("extensor-carpi-radialis", "primary"), ("extensor-carpi-ulnaris", "primary"),
                 ("extensor-digitorum", "primary"), ("common-extensor-tendon", "primary")],
        joints=[("wrist-joint", "extension")], equipment=["dumbbell", "table"],
        instructions=("1. Rest the forearm on a table, hand over the edge, palm down, holding a light weight.\n"
                      "2. Use the other hand to lift the wrist to full extension.\n"
                      "3. Slowly lower the weight over 3-4 seconds using only the involved side.\n"
                      "4. Assist back up and repeat."),
        breathing="Exhale during the slow lowering phase.",
        safety="Start with 0.5-1 kg; expect mild discomfort only, never sharp pain.",
        clinical="Heavily studied eccentric loading protocol for lateral elbow tendinopathy.",
        dosage="3 x 15, daily or every other day"),
    dict(slug="eccentric-wrist-flexion", name="Eccentric Wrist Flexion",
        aliases=["eccentric golfer's elbow exercise"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="seated",
        regions=[("forearm", "primary")],
        muscles=[("flexor-carpi-radialis", "primary"), ("flexor-carpi-ulnaris", "primary"),
                 ("common-flexor-tendon", "primary")],
        joints=[("wrist-joint", "flexion")], equipment=["dumbbell", "table"],
        instructions=("1. Rest the forearm on a table, palm up, hand over the edge with a light weight.\n"
                      "2. Assist the wrist up into flexion with the free hand.\n"
                      "3. Lower slowly over 3-4 seconds under the involved side's control.\n"
                      "4. Assist up again; keep reps smooth."),
        breathing="Exhale while lowering.",
        safety="Very light load to begin; stop with sharp inner-elbow pain.",
        clinical="Eccentric loading variant for medial elbow tendinopathy.",
        dosage="3 x 15"),
    dict(slug="wrist-pronation-supination-mobility", name="Wrist Pronation-Supination Mobility",
        aliases=["forearm rotation mobility", "pronation supination exercise"],
        type="mobility", movement="circumduction", difficulty="beginner", position="seated",
        regions=[("forearm", "primary"), ("elbow", "secondary")],
        muscles=[("pronator-teres", "primary"), ("supinator", "primary"),
                 ("biceps-brachii", "secondary")],
        joints=[("radioulnar-joint", "pronation"), ("radioulnar-joint", "supination")],
        equipment=[("stick",)],
        instructions=("1. Bend the elbow to 90°, tucked at your side; hold a light stick upright.\n"
                      "2. Slowly rotate the forearm palm-down (pronation), like a doorknob.\n"
                      "3. Rotate palm-up (supination) through full comfortable range.\n"
                      "4. Alternate slowly for 10-15 cycles."),
        breathing="Relaxed.",
        safety="Keep the upper arm still; motion is at the forearm only.",
        dosage="2 x 15 slow cycles"),
    dict(slug="radial-deviation-stretch", name="Radial Deviation Stretch (Thumb Side)",
        aliases=["de Quervain stretch", "thumb side wrist stretch", "Finkelstein stretch"],
        type="stretching", movement="adduction", difficulty="beginner", position="standing",
        regions=[("forearm", "primary"), ("wrist", "primary"), ("hand", "secondary")],
        muscles=[("abductor-pollicis-longus", "stretch_target"), ("extensor-pollicis", "stretch_target")],
        joints=[("wrist-joint", "ulnar deviation"), ("thumb-cmc-joint", "flexion")], equipment=[],
        instructions=("1. Make a light fist with the thumb tucked inside the fingers.\n"
                      "2. Bend the wrist toward the pinky side (ulnar deviation).\n"
                      "3. Keep the arm straight in front, shoulder relaxed.\n"
                      "4. Hold 15-20 seconds at a gentle stretch along the thumb base."),
        breathing="Relaxed breathing.",
        safety="Gentle intensity — this stretch can provoke de Quervain symptoms if forced.",
        clinical="Classic self-stretch in de Quervain's tenosynovitis programmes (Finkelstein-based).",
        dosage="3 x 20 seconds per side"),
    dict(slug="forearm-extensor-self-massage", name="Forearm Extensor Self-Massage",
        aliases=["forearm massage tennis elbow", "lateral forearm release"],
        type="release", movement=None, difficulty="beginner", position="seated",
        regions=[("forearm", "primary"), ("elbow", "secondary")],
        muscles=[("extensor-carpi-radialis", "stretch_target"), ("common-extensor-tendon", "stretch_target"),
                 ("brachioradialis", "secondary")],
        joints=[("elbow-joint", None)], equipment=["massage-ball", "table"],
        instructions=("1. Rest the forearm on a table, palm down, with a ball under the outer forearm.\n"
                      "2. Slowly roll along the muscle belly from elbow to mid-forearm.\n"
                      "3. Pause 20-30 seconds on tender spots, breathing slowly.\n"
                      "4. Flex and extend the fingers while paused to release deeper."),
        breathing="Long exhales on tender spots.",
        safety="Avoid rolling directly on the bony elbow point or on swollen tissue.",
        dosage="2-3 minutes per arm"),
    dict(slug="brachioradialis-stretch", name="Brachioradialis Stretch",
        aliases=["forearm flexor radial stretch"],
        type="stretching", movement="pronation", difficulty="intermediate", position="standing",
        regions=[("forearm", "primary")],
        muscles=[("brachioradialis", "stretch_target")],
        joints=[("elbow-joint", "extension"), ("radioulnar-joint", "pronation")], equipment=[],
        instructions=("1. Extend the arm straight, palm down, thumb pointing down (pronated).\n"
                      "2. Grasp the thumb side of the hand and pull the wrist into flexion + ulnar deviation.\n"
                      "3. Keep the elbow fully straight.\n"
                      "4. Hold 20-30 seconds."),
        breathing="Relaxed.",
        safety="A very targeted stretch — keep it mild.",
        dosage="3 x 25 seconds per side"),
    dict(slug="supinator-stretch", name="Supinator Stretch",
        aliases=["forearm pronation stretch"],
        type="stretching", movement="pronation", difficulty="beginner", position="standing",
        regions=[("forearm", "primary")],
        muscles=[("supinator", "stretch_target"), ("biceps-brachii", "secondary")],
        joints=[("radioulnar-joint", "pronation")], equipment=["stick"],
        instructions=("1. Stand with the stick vertical, grasped palm-up (supinated).\n"
                      "2. Keeping the elbow straight, rotate the stick a half turn away from you.\n"
                      "3. The forearm moves into pronation, stretching the supinator.\n"
                      "4. Hold 20 seconds and repeat."),
        breathing="Steady.",
        safety="Rotate only to comfortable pronation.",
        dosage="3 x 20 seconds per side"),
    dict(slug="median-nerve-glide", name="Median Nerve Glide",
        aliases=["banner exercise", "median nerve flossing", "nerve floss median"],
        type="rehabilitation", movement="extension", difficulty="intermediate", position="standing",
        regions=[("wrist", "primary"), ("forearm", "secondary"), ("shoulder", "secondary")],
        muscles=[("median-nerve", "stretch_target")],
        joints=[("wrist-joint", "extension"), ("elbow-joint", "extension")], equipment=[],
        instructions=("1. Make a soft fist around your thumb, arm out to the side at shoulder height.\n"
                      "2. Bend the head away from the arm as you slowly straighten the elbow.\n"
                      "3. Feel a gentle 'slide' — never a stretch — through the arm.\n"
                      "4. Return before any tingling; glide 10-12 times."),
        breathing="Slow and continuous.",
        safety="Nerves need flossing, not stretching: stay below symptom threshold at all times.",
        contra="Do not push into numbness or tingling; stop if symptoms worsen afterwards.",
        clinical="Neural mobilisation used for median-nerve-sensitive presentations incl. carpal tunnel.",
        dosage="10-12 gentle glides"),
    dict(slug="ulnar-nerve-glide", name="Ulnar Nerve Glide",
        aliases=["okay sign nerve glide", "ulnar nerve flossing"],
        type="rehabilitation", movement="flexion", difficulty="intermediate", position="standing",
        regions=[("wrist", "primary"), ("elbow", "secondary")],
        muscles=[("ulnar-nerve", "stretch_target")],
        joints=[("elbow-joint", "flexion"), ("wrist-joint", "extension")], equipment=[],
        instructions=("1. Make the 'OK' sign: thumb and index touching, other three fingers extended.\n"
                      "2. Bring the hand toward your ear, elbow bending out to the side, like holding a phone.\n"
                      "3. Slowly straighten the arm slightly and re-bend — a gentle seesaw.\n"
                      "4. Keep intensity minimal; glide 10 times."),
        breathing="Relaxed.",
        safety="Any inner-elbow tingling means back off — glide within comfort only.",
        contra="Avoid aggravating cubital tunnel symptoms.",
        dosage="10 gentle glides"),
    dict(slug="radial-nerve-glide", name="Radial Nerve Glide",
        aliases=["thumb out nerve glide", "radial nerve flossing"],
        type="rehabilitation", movement="extension", difficulty="intermediate", position="standing",
        regions=[("forearm", "primary"), ("wrist", "secondary")],
        muscles=[("radial-nerve", "stretch_target")],
        joints=[("elbow-joint", "extension"), ("wrist-joint", "extension")], equipment=[],
        instructions=("1. Touch the back of your hand to your temple, thumb pointing down.\n"
                      "2. Slowly reach the hand diagonally up-and-out, elbow straightening.\n"
                      "3. Keep the motion smooth, like polishing a diagonal sky.\n"
                      "4. 10 easy glides, no tingling."),
        breathing="Continuous.",
        safety="Glide, don't stretch; the radial nerve dislikes force.",
        dosage="10 gentle glides"),
    # --------------------------------------------------------------- wrist
    dict(slug="wrist-circles", name="Wrist Circles",
        aliases=["wrist rotations", "wrist mobility circles"],
        type="mobility", movement="circumduction", difficulty="beginner", position="seated or standing",
        regions=[("wrist", "primary")],
        muscles=[("wrist-flexors-generic", "primary"), ("wrist-extensors-generic", "primary")],
        joints=[("wrist-joint", "circumduction")], equipment=[],
        instructions=("1. Extend the arms, make soft fists.\n"
                      "2. Circle the wrists slowly, 10 each direction.\n"
                      "3. Keep the forearms still.\n"
                      "4. Reverse direction midway."),
        breathing="Easy and rhythmic.",
        safety=None,
        dosage="10 circles each direction"),
    dict(slug="prayer-stretch", name="Prayer Stretch",
        aliases=["palms together wrist stretch", "prayer wrist extension stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="standing",
        regions=[("wrist", "primary"), ("forearm", "secondary")],
        muscles=[("flexor-carpi-radialis", "stretch_target"), ("flexor-carpi-ulnaris", "stretch_target")],
        joints=[("wrist-joint", "extension")], equipment=[],
        instructions=("1. Place palms together in front of the chest, elbows out.\n"
                      "2. Keeping palms touching, lower the hands until the wrists stretch.\n"
                      "3. Keep pressure equal on both palms.\n"
                      "4. Hold 20-30 seconds."),
        breathing="Steady; soften on exhale.",
        safety="Keep elbows high enough to feel the wrist, not elbow, stretch.",
        dosage="3 x 30 seconds"),
    dict(slug="tabletop-wrist-stretch", name="Tabletop Wrist Stretch",
        aliases=["wall wrist flexion stretch", "hands flat wrist stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="standing",
        regions=[("wrist", "primary"), ("forearm", "secondary")],
        muscles=[("wrist-flexors-generic", "stretch_target"), ("flexor-retinaculum", "secondary")],
        joints=[("wrist-joint", "extension")], equipment=["table", "wall"],
        instructions=("1. Place hands flat on a table, fingers pointing back toward you.\n"
                      "2. Lean gently forward, keeping palms flat.\n"
                      "3. Stop at a comfortable stretch through the wrist crease and forearm.\n"
                      "4. Hold 20-30 seconds."),
        breathing="Breathe out as you lean.",
        safety="Progress angle slowly; wrists adapt over weeks.",
        contra="Modify with a fist-on-table version if the flat-hand version provokes symptoms.",
        dosage="3 x 30 seconds"),
    dict(slug="wrist-extensor-isometric", name="Wrist Extensor Isometric",
        aliases=["tennis elbow isometric"],
        type="physiotherapy", movement="extension", difficulty="beginner", position="seated",
        regions=[("forearm", "primary")],
        muscles=[("extensor-carpi-radialis", "primary"), ("extensor-carpi-ulnaris", "primary"),
                 ("common-extensor-tendon", "primary")],
        joints=[("wrist-joint", "extension")], equipment=["table"],
        instructions=("1. Rest the forearm on a table, palm down, wrist straight.\n"
                      "2. Press the back of the hand down into the other palm (or table edge).\n"
                      "3. Match force with the resistance — the wrist does not move.\n"
                      "4. Hold 10-30 seconds at a moderate, pain-free effort."),
        breathing="Do not hold the breath.",
        safety="Isometrics should reduce, not raise, elbow pain; if pain increases, lower the force.",
        clinical="Isometric loading is an early-stage analgesic protocol for tendinopathy.",
        dosage="5 x 30 seconds"),
    # ---------------------------------------------------------------- hand
    dict(slug="finger-spread", name="Finger Spread",
        aliases=["finger abduction exercise", "hand fan stretch"],
        type="mobility", movement="abduction", difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("interossei-hand", "primary"), ("lumbricals-hand", "primary")],
        joints=[("finger-mcp-joints", "abduction")], equipment=[],
        instructions=("1. Place the hand flat on a table, palm down.\n"
                      "2. Spread the fingers apart as far as comfortable.\n"
                      "3. Hold 3-5 seconds, then bring them back together.\n"
                      "4. Repeat rhythmically."),
        breathing="Relaxed.",
        safety=None,
        dosage="2 x 15 spreads"),
    dict(slug="fist-to-fan", name="Fist to Fan",
        aliases=["full fist closure exercise", "finger flexion extension mobility"],
        type="mobility", movement="flexion", difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("flexor-digitorum-superficialis", "primary"), ("extensor-digitorum", "primary"),
                 ("lumbricals-hand", "secondary")],
        joints=[("finger-mcp-joints", "flexion"), ("finger-ip-joints", "flexion")], equipment=[],
        instructions=("1. Open the hand wide, fingers spread.\n"
                      "2. Slowly curl into a full, tight fist, thumb outside.\n"
                      "3. Squeeze 2 seconds, then explode gently open into the fan.\n"
                      "4. Repeat 10-15 times."),
        breathing="Exhale on the fist close.",
        safety=None,
        dosage="2 x 15"),
    dict(slug="tendon-gliding-exercise", name="Finger Tendon Gliding Exercise",
        aliases=["flexor tendon glide", "tendon glides", "straight fist hook fist glide"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("flexor-digitorum-superficialis", "primary"), ("flexor-digitorum-profundus", "primary"),
                 ("lumbricals-hand", "secondary")],
        joints=[("finger-ip-joints", "flexion")], equipment=[],
        instructions=("1. Start with fingers straight (straight position).\n"
                      "2. Bend only the big knuckles — 'table top'.\n"
                      "3. Then hook the fingers — 'hook fist'.\n"
                      "4. Then full fist, then straight fist; flow 5-10 cycles."),
        breathing="Easy and slow.",
        safety="Move through comfortable ranges; no forcing swollen or injured joints.",
        clinical="Standard flexor-tendon and carpal-tunnel rehabilitation gliding sequence.",
        dosage="5-10 cycles, several times daily"),
    dict(slug="thumb-stretch-series", name="Thumb Stretch Series",
        aliases=["thumb extension stretch", "opposition stretch"],
        type="stretching", movement="extension", difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("adductor-pollicis", "stretch_target"), ("thenar-muscles", "stretch_target"),
                 ("flexor-pollicis-longus", "secondary")],
        joints=[("thumb-cmc-joint", "extension"), ("thumb-cmc-joint", "abduction")], equipment=[],
        instructions=("1. Gently pull the thumb back and away from the palm (extension/abduction).\n"
                      "2. Hold 10-15 seconds.\n"
                      "3. Then tuck the thumb across the palm under the fingers for 10-15 seconds.\n"
                      "4. Repeat the series 3 times."),
        breathing="Relaxed.",
        safety="Very gentle — thumb joints are small.",
        clinical="Used in first-carpometacarpal (basal thumb) osteoarthritis programmes.",
        dosage="3 x 15 seconds each direction"),
    dict(slug="thenar-self-massage", name="Thenar Self-Massage",
        aliases=["thumb pad massage"],
        type="release", movement=None, difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("thenar-muscles", "stretch_target"), ("adductor-pollicis", "secondary")],
        joints=[("thumb-cmc-joint", None)], equipment=[],
        instructions=("1. Use the opposite thumb to make slow circles on the fleshy thumb pad.\n"
                      "2. Work from the wrist to the thumb joint.\n"
                      "3. Pause 20 seconds on tender knots.\n"
                      "4. Finish by moving the thumb through its circle (opposition)."),
        breathing="Slow.",
        safety="Avoid pressing on numb or tingling areas.",
        dosage="1-2 minutes per hand"),
    dict(slug="towel-squeeze", name="Towel Squeeze",
        aliases=["grip exercise towel", "hand grip strengthening"],
        type="strength", movement="flexion", difficulty="beginner", position="seated",
        regions=[("hand", "primary"), ("forearm", "secondary")],
        muscles=[("flexor-digitorum-superficialis", "primary"), ("flexor-digitorum-profundus", "primary"),
                 ("thenar-muscles", "secondary"), ("adductor-pollicis", "stabilizer")],
        joints=[("finger-mcp-joints", "flexion")], equipment=["towel"],
        instructions=("1. Roll a small towel and hold it in one hand.\n"
                      "2. Squeeze firmly for 3-5 seconds.\n"
                      "3. Release partially and repeat.\n"
                      "4. Keep the wrist neutral throughout."),
        breathing="Exhale on squeeze.",
        safety="Avoid maximal gripping with acute tendon irritation.",
        dosage="3 x 12-15"),
    dict(slug="marble-pickup", name="Marble Pickup",
        aliases=["object pickup exercise", "intrinsic hand exercise marbles"],
        type="rehabilitation", movement="flexion", difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("lumbricals-hand", "primary"), ("interossei-hand", "primary"),
                 ("flexor-digitorum-profundus", "secondary")],
        joints=[("finger-mcp-joints", "flexion"), ("finger-ip-joints", "flexion")],
        equipment=["marbles"],
        instructions=("1. Place 10-20 marbles (or beans) on one side of a bowl.\n"
                      "2. Pick them up one at a time with a pincer or full-grip and move them across.\n"
                      "3. Work with focus on controlled finger motion.\n"
                      "4. Reverse hands and repeat."),
        breathing="Relaxed.",
        safety=None,
        dosage="2-3 rounds per hand"),
    dict(slug="finger-extension-rubber-band", name="Finger Extension With Rubber Band",
        aliases=["rubber band finger exercise", "hand extension exercise"],
        type="strength", movement="extension", difficulty="beginner", position="seated",
        regions=[("hand", "primary")],
        muscles=[("extensor-digitorum", "primary"), ("interossei-hand", "secondary"),
                 ("lumbricals-hand", "secondary")],
        joints=[("finger-mcp-joints", "extension")], equipment=["resistance-band"],
        instructions=("1. Loop a light rubber band around all five fingertips.\n"
                      "2. Spread the fingers open against the band's resistance.\n"
                      "3. Hold 2 seconds, return slowly.\n"
                      "4. Keep the band light — this is endurance, not max force."),
        breathing="Steady.",
        safety="Point bands away from the face.",
        dosage="3 x 15"),
]
