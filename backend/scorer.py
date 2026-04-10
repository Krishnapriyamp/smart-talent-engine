from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 🔥 Better model (optional upgrade)
model = SentenceTransformer('all-MiniLM-L6-v2')
# You can upgrade to: 'all-mpnet-base-v2' for better results


# =========================
# 🧠 TEXT CLEANING
# =========================

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    return text


# =========================
# 🧠 EMBEDDING
# =========================

def embed(text):
    text = clean_text(text)
    vec = model.encode([text])[0]

    # 🔥 normalize vector (important)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


# =========================
# 🧠 SEMANTIC SCORE
# =========================

def semantic_score(jd, cand):
    jd_vec = embed(jd)
    cand_vec = embed(cand)

    score = cosine_similarity([jd_vec], [cand_vec])[0][0]

    return float(score * 100)


# =========================
# 🧠 SKILL SCORE
# =========================

def skill_score(jd_skills, cand_skills):
    if not jd_skills:
        return 50

    # 🔥 Fix: Convert to lowercase for case-insensitive matching
    jd_skills_lower = [s.lower().strip() for s in jd_skills]
    cand_skills_lower = [s.lower().strip() for s in cand_skills]

    # 🔥 Partial matching synonyms
    synonyms = {
        "ml": "machine learning",
        "machine learning": "ml",
        "data analytics": "data analysis",
        "data analysis": "data analytics",
        "nlp": "natural language processing",
        "natural language processing": "nlp",
        "deep learning": "dl",
        "dl": "deep learning",
        "data science": "ds",
        "ds": "data science",
        "software engineering": "se",
        "se": "software engineering",
        "visualization": "viz",
        "viz": "visualization",
    }

    # Expand skills with synonyms
    def expand_skills(skills):
        expanded = set(skills)
        for skill in skills:
            if skill in synonyms:
                expanded.add(synonyms[skill])
        return expanded

    jd_expanded = expand_skills(jd_skills_lower)
    cand_expanded = expand_skills(cand_skills_lower)

    matched = jd_expanded.intersection(cand_expanded)
    missing = jd_expanded - cand_expanded

    skill_weights = {
        "python": 2.0,
        "sql": 2.0,
        "machine learning": 2.0,
        "data science": 1.8,
        "deep learning": 1.8,
        "pandas": 1.5,
        "numpy": 1.5,
        "visualization": 1.4,
        "nlp": 1.5,
        "tensorflow": 1.7,
        "pytorch": 1.7,
        "scikit-learn": 1.6,
        "data analysis": 1.4,
        "statistics": 1.4,
        "software engineering": 1.3,
        # Add lowercase versions and synonyms
        "ml": 2.0,
        "ds": 1.8,
        "dl": 1.8,
        "se": 1.3,
        "viz": 1.4,
        "natural language processing": 1.5,
        "data analytics": 1.4,
    }

    total_weight = sum(skill_weights.get(skill, 1.0) for skill in jd_expanded)
    matched_weight = sum(skill_weights.get(skill, 1.0) for skill in matched)

    base_score = (matched_weight / total_weight) * 100 if total_weight > 0 else 0
    bonus = 0

    # 🔥 Update bonuses to use lowercase
    if "python" in matched:
        bonus += 8
    if "sql" in matched:
        bonus += 7
    if "machine learning" in matched or "ml" in matched or "data science" in matched or "ds" in matched:
        bonus += 6

    related_pairs = [
        ("machine learning", "deep learning"),
        ("machine learning", "statistics"),
        ("data analysis", "visualization"),
        ("data science", "pandas"),
        ("data science", "numpy"),
        ("deep learning", "pytorch"),
        ("deep learning", "tensorflow"),
        ("nlp", "text processing"),
        # Add lowercase pairs
        ("ml", "dl"),
        ("ml", "statistics"),
        ("data analysis", "viz"),
        ("ds", "pandas"),
        ("ds", "numpy"),
        ("dl", "pytorch"),
        ("dl", "tensorflow"),
        ("nlp", "text processing"),
    ]
    for a, b in related_pairs:
        if a in jd_expanded and b in cand_expanded and b not in matched:
            bonus += 5
        if b in jd_expanded and a in cand_expanded and a not in matched:
            bonus += 5

    if len(matched) == len(jd_expanded) and len(jd_expanded) > 0:
        bonus += 8

    score = base_score + bonus
    # 🔥 Ensure score is not zero if there's any overlap
    if matched and score == 0:
        score = 10  # Minimum score for any match
    return min(max(score, 0), 100)


# =========================
# 🧠 EXPERIENCE SCORE
# =========================

def experience_score(jd_exp, cand_exp):
    years = cand_exp.get("years", 0)
    projects = cand_exp.get("projects", 0)
    certifications = cand_exp.get("certifications", 0)
    work_exp = cand_exp.get("work_exp", 0)

    if jd_exp and jd_exp > 0:
        years_score = min(years / jd_exp, 1) * 100
    else:
        years_score = min(years * 15, 100)

    bonus = projects * 5 + certifications * 3 + work_exp * 7
    score = years_score + bonus

    return min(max(score, 0), 100)


# =========================
# 🧠 FINAL SCORE
# =========================

def final_score(sem, skill, exp, boost=0):
    return 0.35 * sem + 0.40 * skill + 0.25 * exp + boost


# =========================
# 🧠 CONFIDENCE
# =========================

def confidence_score(sem, skill, exp):
    return min(max(0.3 * sem + 0.4 * skill + 0.3 * exp, 0), 100)


# =========================
# 🚨 SEMANTIC ADJUSTMENT
# =========================

def adjust_semantic(sem):
    if sem > 60:
        return min(100, sem + (sem - 60) * 0.12)
    return sem


def penalty_score(jd_skills, cand_skills, matched_skills, missing_skills, sem_score, skill_score):
    # 🔥 Do not apply penalty if semantic score > 60
    if sem_score > 60:
        return 0

    penalty = 0

    # 🔥 Only apply penalty for critical missing skills
    critical_skills = {"python", "sql"}
    cand_lower = [s.lower() for s in cand_skills]
    for skill in critical_skills:
        if skill.lower() in [s.lower() for s in jd_skills] and skill not in cand_lower:
            penalty += 10  # Reduced from 12

    # 🔥 Reduce penalty for low skill score
    if skill_score < 40:
        penalty += 10  # Instead of heavier penalties

    # 🔥 Lighter penalties for missing skills
    if len(missing_skills) >= 2:
        penalty += 5  # Reduced from 7
    if len(missing_skills) >= 4:
        penalty += 5  # Reduced from 8

    if len(matched_skills) == 0:
        penalty += 5  # Reduced from 10

    return min(penalty, 20)  # Cap at 20 instead of 30