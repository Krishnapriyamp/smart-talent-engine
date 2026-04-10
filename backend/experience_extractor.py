import re
from datetime import datetime
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

def calculate_experience(text):
    """
    Calculate total work experience in years from resume text.
    Parses date ranges and sums up durations.
    """
    text = text.lower()
    total_years = 0.0

    # Count internships and work experiences
    internship_count = len(re.findall(r'\b(?:internship|intern)\b', text))
    work_experience_count = len(re.findall(r'\b(?:worked|employed|experience|developer|engineer|analyst|scientist)\b', text))

    # Patterns for date ranges
    date_patterns = [
        # Full ranges: Jan 2023 - Jun 2023, 01/2023 - 06/2023, etc.
        r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4})',
        r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4})',
        r'(\d{4})\s*[-–]\s*(\d{4})',
    ]

    extracted_periods = []
    processed_years = set()

    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                start_str, end_str = match
                try:
                    # Parse dates more carefully
                    start_date = date_parser.parse(start_str, default=datetime(2000, 1, 1))
                    end_date = date_parser.parse(end_str, default=datetime(2000, 1, 1))

                    # If only year was provided, assume Jan 1 to Dec 31
                    if start_str.isdigit() and len(start_str) == 4:
                        start_date = datetime(int(start_str), 1, 1)
                        end_date = datetime(int(end_str), 12, 31)
                    elif end_str.isdigit() and len(end_str) == 4:
                        end_date = datetime(int(end_str), 12, 31)

                    duration = (end_date - start_date).days / 365.25

                    # For internships or if duration is very short, assume 6 months
                    if duration < 0.2:  # Less than ~2 months
                        duration = 0.5
                    elif duration > 10:  # Unreasonable
                        continue

                    extracted_periods.append(duration)
                except:
                    continue

    # If we found date ranges, use those
    if extracted_periods:
        total_years = sum(extracted_periods)
    else:
        # Fallback: count unique years and assume 6 months per internship/work experience
        years = set(re.findall(r'\b(20\d{2})\b', text))
        years_with_context = set()

        # Only count years that appear near work-related keywords
        for year in years:
            year_pattern = rf'\b{year}\b'
            context_window = 50  # characters around the year
            for match in re.finditer(year_pattern, text):
                start = max(0, match.start() - context_window)
                end = min(len(text), match.end() + context_window)
                context = text[start:end]
                if any(keyword in context for keyword in ['intern', 'worked', 'employed', 'experience', 'developer', 'engineer', 'analyst', 'scientist']):
                    years_with_context.add(year)

        total_years = len(years_with_context) * 0.5

    # Additional boost for multiple internships in same year
    internship_count = len(re.findall(r'\b(?:internship|intern)\b', text))
    if internship_count > 1 and total_years < internship_count * 0.5:
        total_years = internship_count * 0.5

    # Fallback: look for explicit year mentions
    if total_years == 0:
        years_matches = re.findall(r'(\d+(?:\.\d+)?)(?:\+)?\s*(?:years?|yrs?|yr)\b', text)
        if years_matches:
            total_years = max([float(y) for y in years_matches])

    return round(total_years, 2)

def extract_experience_details(text):
    text = text.lower()

    work_exp_patterns = [
        r"\binternship\b",
        r"\bintern\b",
        r"\bworked at\b",
        r"\bworked as\b",
        r"\bworked in\b",
        r"\bexperience at\b",
        r"\bexperience in\b",
        r"\bemployed at\b",
        r"\bfull[- ]time\b",
        r"\bpart[- ]time\b",
        r"\bconsultant\b",
        r"\bfreelance\b",
        r"\bcontract\b",
    ]
    work_exp = sum(len(re.findall(pattern, text)) for pattern in work_exp_patterns)

    project_patterns = [
        r"\bproject\b",
        r"\bdeveloped\b",
        r"\bbuilt\b",
        r"\bimplemented\b",
        r"\bdesigned\b",
        r"\bled\b",
        r"\bengineered\b",
    ]
    projects = sum(len(re.findall(pattern, text)) for pattern in project_patterns)

    certification_patterns = [
        r"\bcertification\b",
        r"\bcertified\b",
        r"\bcourse\b",
        r"\bbootcamp\b",
        r"\bdiploma\b",
    ]
    certifications = sum(len(re.findall(pattern, text)) for pattern in certification_patterns)

    # Use the new calculate_experience function
    total_years = calculate_experience(text)

    return {
        "years": total_years,
        "projects": projects,
        "certifications": certifications,
        "work_exp": work_exp,
    }