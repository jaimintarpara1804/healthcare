def suggest_yoga(disease):
    disease = (disease or "").lower()
    yoga_map = {
        "diabetes": ["Surya Namaskar", "Dhanurasana", "Paschimottanasana"],
        "asthma": ["Bhujangasana", "Ardha Matsyendrasana", "Sukhasana"],
        "back pain": ["Cat-Cow Pose", "Child's Pose", "Bridge Pose"],
        "stress": ["Padmasana", "Shavasana", "Anulom Vilom"]
    }
    for key in yoga_map:
        if key in disease:
            return yoga_map[key]
    return ["No specific yoga found, try consulting an instructor."]
