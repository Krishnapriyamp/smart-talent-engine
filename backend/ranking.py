try:
    from scorer import *
    from llm_justification import generate_justification
except ImportError:
    from scorer import *
    from llm_justification import generate_justification

def get_verdict(score):
    if score >= 75:
        return "Highly Suitable"
    elif score >= 55:
        return "Moderately Suitable"
    else:
        return "Not Suitable"

def get_score_color(score):
    if score >= 70:
        return "green"
    elif score >= 40:
        return "orange"
    else:
        return "red"

def rank_candidates(jd, candidates):
    results = []

    for c in candidates:
        # 🔥 Ensure texts are not empty
        jd_text = jd.get("text", "").strip()
        cand_text = c.get("raw_text", "").strip()
        if not jd_text or not cand_text:
            sem = 30  # Minimum score
        else:
            sem = adjust_semantic(semantic_score(jd_text, cand_text))

        skill = skill_score(jd["skills"], c["skills"])
        exp = experience_score(jd["experience"], c["experience"])

        # 🔥 Normalize minimum scores
        sem = max(sem, 30)
        skill = max(skill, 20)
        exp = max(exp, 20)

        # 🔥 Fix: Use lowercase for matching
        jd_skills_lower = [s.lower().strip() for s in jd.get("skills", [])]
        cand_skills_lower = [s.lower().strip() for s in c.get("skills", [])]
        matched = sorted(list(set(jd_skills_lower).intersection(set(cand_skills_lower))))
        missing = sorted(list(set(jd_skills_lower) - set(cand_skills_lower)))

        boost = 0
        if jd["skills"] and len(matched) == len(jd["skills"]):
            boost += 8

        # 🔥 Boost for strong candidates
        if sem > 60 and skill > 60:
            boost += 10
        if len(matched) >= 3:
            boost += 5

        penalty = penalty_score(jd["skills"], c["skills"], matched, missing, sem, skill)

        final = final_score(sem, skill, exp, boost) - penalty
        final = min(max(final, 0), 100)
        confidence = confidence_score(sem, skill, exp)

        explanation = generate_justification(
            matched,
            missing,
            c["experience"],
            final
        )

        # Generate dynamic explanation based on score and missing skills
        if final >= 85 and not missing:
            explanation_text = "Candidate is highly suitable with strong alignment in skills and experience."
        elif 60 <= final < 85:
            explanation_text = "Candidate shows good fit but has some gaps to address."
        else:
            explanation_text = "Candidate has limited alignment with job requirements."

        # Add semantic justification if applicable
        if sem < 50 and skill > 80:
            explanation_text += " Semantic similarity is moderate due to variation in wording, but strong skill match compensates."

        # Generate weakness based on experience
        exp_years = c["experience"].get("years", 0)
        if exp_years < 1:
            weakness = "Early career candidate (internship-level experience)"
        elif 1 <= exp_years <= 3:
            weakness = "Limited professional experience"
        else:
            weakness = "No major weaknesses"

        confidence_explanation = "Confidence indicates model certainty based on resume clarity and matching consistency."

        results.append({
            "name": c["name"],

            "score": round(final, 2),
            "confidence": round(confidence, 2),

            "semantic": round(sem, 2),
            "skill": round(skill, 2),
            "experience_score": round(exp, 2),

            "matched_skills": matched,
            "missing_skills": missing,
            "skills": c.get("skills", []),
            "extracted_skills": c.get("skills", []),

            "exp_details": c.get("experience", {}),
            "experience": c.get("experience", {}),

            "penalty": penalty,
            "verdict": get_verdict(final),
            "color": get_score_color(final),

            "explanation": explanation_text,
            "strengths": explanation.get("strengths", []),
            "weaknesses": [weakness],
            "confidence_explanation": confidence_explanation,
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)