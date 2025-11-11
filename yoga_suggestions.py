def suggest_yoga(text: str):
    """
    Very simple keyword-based mapping.
    Lowercases the input, returns list of asanas/breathing.
    """
    if not text:
        return ["No specific yoga found, try consulting an instructor."]

    t = text.lower()

    yoga_dict = {
        "diabetes": [
            "Surya Namaskar (Sun Salutation)",
            "Dhanurasana (Bow Pose)",
            "Paschimottanasana (Seated Forward Bend)"
        ],
        "asthma": [
            "Bhujangasana (Cobra Pose)",
            "Ardha Matsyendrasana (Half Spinal Twist)",
            "Anulom Vilom (Alternate Nostril Breathing)"
        ],
        "back pain": [
            "Marjaryasana-Bitilasana (Cat–Cow)",
            "Balasana (Child’s Pose)",
            "Setu Bandhasana (Bridge Pose)"
        ],
        "stress": [
            "Padmasana (Lotus Pose)",
            "Shavasana (Corpse Pose)",
            "Bhramari Pranayama (Humming Bee Breath)"
        ],
        "anxiety": [
            "Padmasana (Lotus Pose)",
            "Shavasana (Corpse Pose)",
            "Bhramari Pranayama (Humming Bee Breath)"
        ],
        "headache": [
            "Uttanasana (Standing Forward Bend)",
            "Viparita Karani (Legs-up-the-wall)",
            "Nadi Shodhana (Alternate Nostril Breathing)"
        ],
        "cold": [
            "Kapalabhati (Skull Shining)",
            "Ardha Matsyendrasana (Half Twist)",
            "Bhujangasana (Cobra Pose)"
        ]
    }

    for key, vals in yoga_dict.items():
        if key in t:
            return vals

    return [
        "Tadasana (Mountain Pose)",
        "Vrikshasana (Tree Pose)",
        "Sukhasana with deep breathing"
    ]
