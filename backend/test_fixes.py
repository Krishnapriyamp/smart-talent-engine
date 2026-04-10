#!/usr/bin/env python3
"""
Manual Testing Script for Smart Talent Selection Engine
Test the experience calculation and skill extraction fixes
"""

from experience_extractor import calculate_experience
from ontology import normalize_skills

def test_experience_calculation():
    """Test experience calculation with various resume texts"""
    print("=" * 60)
    print("🧪 TESTING EXPERIENCE CALCULATION")
    print("=" * 60)

    test_cases = [
        # Internships with years
        ("Data Science Intern 2023 Backend Developer Intern 2023", 1.0),
        ("Software Engineer Intern 2023", 0.5),
        ("Internship 2022 and 2023", 1.0),

        # Date ranges
        ("Software Engineer Jan 2023 - Jun 2023", 0.5),
        ("Data Analyst Jul 2023 - Dec 2023", 0.5),
        ("Full Stack Developer Jan 2022 - Dec 2023", 2.0),

        # Mixed formats
        ("Intern 2023, Developer Jan 2023 - Jun 2023", 1.0),
        ("5 years experience", 5.0),  # Fallback

        # Edge cases
        ("No dates mentioned", 0.0),
        ("Worked in 2020 and 2021", 1.0),  # Assumes 6 months each
    ]

    for text, expected in test_cases:
        result = calculate_experience(text)
        status = "✅" if abs(result - expected) < 0.1 else "❌"
        print(f"{status} '{text}' → {result:.1f} years (expected: {expected:.1f})")

def test_skill_extraction():
    """Test skill extraction with keyword and semantic matching"""
    print("\n" + "=" * 60)
    print("🧪 TESTING SKILL EXTRACTION")
    print("=" * 60)

    test_cases = [
        # Keyword matches
        ("I work with python and sql databases", ["python", "sql"]),
        ("Machine learning and deep learning experience", ["machine learning", "deep learning"]),
        ("Java, C++, and JavaScript development", ["java", "javascript"]),

        # Semantic matches
        ("I analyze data and create visualizations", ["data analysis", "visualization"]),
        ("Data preprocessing and feature engineering", ["data analysis", "data science"]),
        ("Building REST APIs and microservices", ["api", "software engineering"]),

        # Mixed matches
        ("Python programming for data analysis and machine learning", ["python", "data analysis", "machine learning"]),
        ("Cloud computing with AWS and Docker containers", ["cloud", "docker"]),

        # No matches
        ("General work experience", []),
    ]

    for text, expected_keywords in test_cases:
        result = normalize_skills(text)
        # Check if expected keywords are in result (semantic might add extras)
        matched = all(keyword in result for keyword in expected_keywords)
        status = "✅" if matched else "❌"
        print(f"{status} '{text}'")
        print(f"    Expected: {expected_keywords}")
        print(f"    Got: {result}")
        print()

def test_full_pipeline():
    """Test the complete parsing pipeline"""
    print("=" * 60)
    print("🧪 TESTING FULL PIPELINE")
    print("=" * 60)

    # Simulate resume text
    resume_text = """
    John Doe
    Data Science Intern - 2023
    Backend Developer Intern - 2023

    Skills: Python, Machine Learning, SQL
    Experience: Data analysis and visualization projects
    """

    print("Resume Text:")
    print(resume_text.strip())
    print()

    # Test experience
    experience = calculate_experience(resume_text)
    print(f"📅 Calculated Experience: {experience} years")

    # Test skills
    skills = normalize_skills(resume_text)
    print(f"🛠️  Extracted Skills: {skills}")

    print("\n✅ Pipeline test completed!")

if __name__ == "__main__":
    print("🚀 Smart Talent Selection Engine - Manual Testing")
    print("Testing the fixes for experience calculation and skill detection\n")

    test_experience_calculation()
    test_skill_extraction()
    test_full_pipeline()

    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("If you see ❌, there might be issues with the implementation.")
    print("=" * 60)