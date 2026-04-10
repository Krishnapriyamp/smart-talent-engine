def generate_justification(matched_skills, missing_skills, exp_details, score):
    strengths = []
    weaknesses = []

    total_skills = len(matched_skills) + len(missing_skills)
    skill_match_ratio = (len(matched_skills) / total_skills) if total_skills > 0 else 0

    if skill_match_ratio >= 0.7:
        strengths.append("Strong technical fit")
    elif skill_match_ratio >= 0.4:
        strengths.append("Relevant skills present")

    if score >= 75:
        strengths.append("High overall ranking")
    elif score >= 55:
        strengths.append("Moderate fit")

    if exp_details.get("years", 0) >= 3:
        strengths.append("Solid experience level")
    if exp_details.get("projects", 0) >= 2:
        strengths.append("Hands-on project experience")
    if exp_details.get("certifications", 0) > 0:
        strengths.append("Relevant certifications")

    if missing_skills:
        weaknesses.append(f"Missing required skills: {', '.join(missing_skills)}")
        if "python" in missing_skills:
            weaknesses.append("Lacks Python, a critical technical skill")
        if "sql" in missing_skills:
            weaknesses.append("Lacks SQL, key for data roles")

    if exp_details.get("years", 0) < 2:
        weaknesses.append("Limited experience")
    if exp_details.get("work_exp", 0) < 1:
        weaknesses.append("Needs more work or internship experience")

    if len(strengths) == 0 and len(weaknesses) == 0:
        summary = "Candidate shows a fair match with room to grow."
    elif len(strengths) > 0 and len(weaknesses) == 0:
        summary = "Candidate shows a strong alignment with required skills and experience."
    elif len(strengths) > 0:
        summary = "Candidate shows good fit in key areas but has some gaps to address."
    else:
        summary = "Candidate has notable gaps in skills or experience."

    return {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }